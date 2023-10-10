import datetime

from django.db import transaction

from _aspirebase.api.data_utils import UserDataUtils
from _aspirebase.api.utils import BaseApiUtils
from _aspirebase.permission_mixins import check_group_allowed
from _aspirebase.validators import Validators
from aspireloan.api.data_utils import LoanDataUtils
from aspireloan.constants import REPAYMENT_FREQ, PDG, AVD, RJD, LOAN_STATUS, PAID, PMT_STATUS


class LoanUtils:
    loan_data_utils = LoanDataUtils()
    user_data_utils = UserDataUtils()

    def create_loan(self, user, **kwargs):
        if not user:
            return {'error': 'No user found'}, 400
        # We can add check if a request is already in process for a User,
        # new request cannot be taken
        amount, valid = Validators.float_validator(kwargs.get('amount'))
        if not valid or amount <= 0:
            return {'error': 'Please provide a valid loan amount'}, 400
        term, valid = Validators.int_validator(kwargs.get('term'))
        if not valid or term <= 0:
            return {'error': 'Please provide a valid loan term'}, 400
        loan_data = {
            'loan_amount': amount,
            'loan_term': term,
            'created_by': user
        }
        loan_terms = []
        term_amount = round(amount / term, 2)
        total_amount = 0
        today = datetime.datetime.now().date()
        for i in range(term):
            if i == term - 1:
                term_amount = amount - total_amount
            total_amount += term_amount
            loan_terms.append({
                'term_amount': term_amount,
                'due_date': today + datetime.timedelta(days=(i + 1) * REPAYMENT_FREQ)
            })
        with transaction.atomic():
            loan = self.loan_data_utils.create_loan(**loan_data)
            for e in loan_terms:
                e['loan'] = loan
            self.loan_data_utils.bulk_create_loan_term(loan_terms)
        return {'message': 'Loan created successfully'}, 200

    def update_loan_status(self, user, **kwargs):
        if not user:
            return {'error': 'No user found'}, 400
        # TODO: add user group check
        user_groups = self.user_data_utils.get_user_groups(user.id)
        if not check_group_allowed(user_groups, ["loan_admin"]):
            return {"error": "You cannot perform this action"}, 400
        loan_id, valid = Validators.int_validator(kwargs.get('loan_id'))
        # Currently we are using primary_key as loan_id, we can replace it with other
        # unique id/ uuid as using primary_key is not a good idea in general,
        # since it will be used by out internal user (admin) hence taking this leeway
        if not valid:
            return {'error': 'Please provide valid loan id'}, 400
        action = kwargs.get('action')
        if action not in ['approve', 'reject']:
            return {'error': 'Please choose a valid action'}, 400
        loan = self.loan_data_utils.get_loan(**{
            'pk': loan_id
        })
        if not loan:
            return {'error': 'No loan found with the provided id'}, 400
        if not loan.status == PDG:
            return {'error': 'Loan status can not be changed now'}, 400
        if action == 'approve':
            loan.status = AVD
        else:
            loan.status = RJD
        loan.approved_by = user
        loan.approved_at = datetime.datetime.now()
        loan.save(update_fields=['status', 'approved_by', 'approved_at'])
        return {'message': 'Loan status updated successfully'}, 200

    def list_user_loans(self, user, **kwargs):
        if not user:
            return {'error': 'No user found'}, 400
        filters = {'created_by': user}
        status = kwargs.get('status')
        if status:
            status = status.upper().replace(" ", "")
            status = status.split(',')
            allowed_status = list(dict(LOAN_STATUS).keys())
            if set(status) - set(allowed_status):
                return {'error': 'Please select valid loan status'}, 400
            filters.update({'status__in': status})
        loans = self.loan_data_utils.filter_loan(**filters).values(
            'loan_amount', 'paid_amount', 'loan_term', 'status',
            'created_at', 'id').order_by('-created_at')
        page = kwargs.get('page', 1)
        limit = kwargs.get('limit', 10)
        paginated_data, pagination = BaseApiUtils.get_paginator(page, loans, limit)
        loan_status_dict = dict(LOAN_STATUS)
        for data in paginated_data:
            data['status'] = loan_status_dict[data['status']]
        return {'data': paginated_data, 'pagination': pagination}, 200

    def loan_repayment(self, **kwargs):
        term_id, valid = Validators.int_validator(kwargs.get('term_id'))
        if not valid:
            return {'error': 'Please provide a valid loan term id'}, 400
        amount, valid = Validators.float_validator(kwargs.get('amount'))
        if not valid or amount <= 0:
            return {'error': 'Please send a valid amount for repayment'}, 400
        loan_term = self.loan_data_utils.get_loan_term(**{'pk': term_id})
        if loan_term.status == PAID:
            return {'error': 'Payment against selected schedule is already completed'}, 400
        loan = loan_term.loan
        if loan.status == PAID:
            return {'error': 'Loan is already closed'}, 400
        if amount < loan_term.term_amount - loan_term.paid_amount:
            return {'error': 'Minimum amount required for this schedule is '
                             '{}'.format(loan_term.term_amount - loan_term.paid_amount)}, 400
        if amount > loan.loan_amount - loan.paid_amount:
            return {'error': 'Total pending amount against this loan is '
                             '{}'.format(loan.loan_amount - loan.paid_amount)}, 400
        paid_amount = loan_term.term_amount - loan_term.paid_amount
        remaining_amount = amount - paid_amount
        update_loan_terms = []
        # If amount provided is more than schedule payment, then remaining amount
        # will be used to settle other pending schedules, old schedules will be settled first,
        # as they might incur high penalty charges
        if remaining_amount > 0:
            all_loan_terms = self.loan_data_utils.filter_loan_term(**{
                'loan': loan,
                'status': PDG
            }).exclude(pk=term_id).order_by('created_at')
            i = 0
            while remaining_amount > 0:
                e = all_loan_terms[i]
                pending_amt = e.term_amount - e.paid_amount
                amt_to_pay = min(pending_amt, remaining_amount)
                e.paid_amount += amt_to_pay
                if amt_to_pay == pending_amt:
                    e.status = PAID
                update_loan_terms.append(e)
                remaining_amount -= amt_to_pay
                i += 1
        loan_term.paid_amount += paid_amount
        loan_term.status = PAID
        loan.paid_amount += amount
        if loan.paid_amount == loan.loan_amount:
            loan.status = PAID
        loan_repayment_data = {
            'loan': loan,
            'repayment_amount': amount,
            'loan_term_id': loan_term.id
        }
        with transaction.atomic():
            loan.save(update_fields=['paid_amount', 'status'])
            loan_term.save(update_fields=['paid_amount', 'status'])
            if update_loan_terms:
                self.loan_data_utils.bulk_update_loan_term(update_loan_terms, ['paid_amount', 'status'])
            self.loan_data_utils.create_loan_repayment_hist(**loan_repayment_data)
        return {'message': 'Payment completed successfully'}, 200

    def get_loan_details(self, user, loan_id):
        # This is to get the details of a particular loan, it will be used by end consumer,
        # as it need user also, since a user cannot see other user's loan
        if not user:
            return {'error': 'No user found'}, 400
        loan = self.loan_data_utils.get_loan(**{
            'pk': loan_id,
            'created_by': user
        })
        if not loan:
            return {'error': 'No loan found for the given loan id'}, 400
        loan_terms = self.loan_data_utils.filter_loan_term(
            **{'loan': loan}).values('term_amount', 'paid_amount', 'due_date', 'status', 'id')
        loan_status_dict = dict(LOAN_STATUS)
        loan_data = {
            'loan_amount': loan.loan_amount,
            'paid_amount': loan.paid_amount,
            'loan_term': loan.loan_term,
            'status': loan_status_dict[loan.status],
            'created_at': loan.created_at,
            'approved_at': loan.approved_at
        }
        pmt_status_dict = dict(PMT_STATUS)
        for term in loan_terms:
            term['status'] = pmt_status_dict[term['status']]
        resp_data = {
            'loan_data': loan_data,
            'loan_terms': loan_terms
        }
        return {'data': resp_data}, 200
