from aspireloan.models import Loan, LoanTerm, LoanRepaymentHistory


class LoanDataUtils:

    @staticmethod
    def create_loan(**kwargs):
        return Loan.objects.create(**kwargs)

    @staticmethod
    def get_loan(**kwargs):
        try:
            return Loan.objects.get(**kwargs)
        except Loan.DoesNotExist:
            return None
        except Loan.MultipleObjectsReturned:
            # NOTE: if multiple objects are found we can raise an alert or
            # delete that object depending on the requirement
            return None

    @staticmethod
    def filter_loan(**kwargs):
        return Loan.objects.filter(**kwargs)

    @staticmethod
    def bulk_create_loan_term(loan_terms):
        return LoanTerm.objects.bulk_create(
            [LoanTerm(**e) for e in loan_terms], batch_size=500)

    @staticmethod
    def get_loan_term(**kwargs):
        try:
            return LoanTerm.objects.get(**kwargs)
        except LoanTerm.DoesNotExist:
            return None
        except LoanTerm.MultipleObjectsReturned:
            return None

    @staticmethod
    def filter_loan_term(**kwargs):
        return LoanTerm.objects.filter(**kwargs)

    @staticmethod
    def create_loan_repayment_hist(**kwargs):
        return LoanRepaymentHistory.objects.create(**kwargs)

    @staticmethod
    def bulk_update_loan_term(loan_terms, fields):
        return LoanTerm.objects.bulk_update(loan_terms, fields)
