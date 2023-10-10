from django.db import models

from _aspirebase.models import BaseModel
from aspireloan.constants import PDG, LOAN_STATUS, PMT_STATUS


# Create your models here.

class Loan(BaseModel):
    loan_amount = models.FloatField(default=0.0)
    paid_amount = models.FloatField(default=0.0)
    loan_term = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='loan_created_by')
    status = models.CharField(max_length=7, default=PDG, choices=LOAN_STATUS)
    approved_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='loan_approved_by')
    approved_at = models.DateTimeField(null=True, blank=True)
    # NOTE: we can also add reason of rejection, loan required for,
    # multiple loan policies/rules, repayment policies/rules etc. if needed


class LoanTerm(BaseModel):
    loan = models.ForeignKey(
        'aspireloan.Loan', on_delete=models.CASCADE)
    term_amount = models.FloatField(default=0.0)
    paid_amount = models.FloatField(default=0.0)
    due_date = models.DateField()
    status = models.CharField(max_length=7, default=PDG, choices=PMT_STATUS)


class LoanRepaymentHistory(BaseModel):
    loan = models.ForeignKey(
        'aspireloan.Loan', on_delete=models.CASCADE)
    repayment_amount = models.FloatField(default=0.0)
    loan_term_id = models.PositiveIntegerField()  # Payment recorded against the specific schedule
    # NOTE: we can also maintain paid_by, payment_id, payment_mode etc. if needed
