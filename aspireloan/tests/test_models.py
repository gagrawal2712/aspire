from django.test import TestCase

from django.contrib.auth.models import User

from aspireloan.constants import LOAN_STATUS
from aspireloan.models import Loan


class LoanModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        testuser = User.objects.create(
            username='testuser',
            password='12345'
        )
        Loan.objects.create(
            loan_amount=3700,
            paid_amount=567,
            loan_term=5,
            status='PDG',
            created_by=testuser
        )

    def test_paid_amount(self):
        loan = Loan.objects.get(pk=1)
        paid_amount = loan.paid_amount
        loan_amount = loan.loan_amount
        resp = loan_amount >= paid_amount >= 0 and isinstance(paid_amount, float)
        self.assertEqual(resp, True)

    def test_status(self):
        loan = Loan.objects.get(pk=1)
        status = loan.status
        resp = status in dict(LOAN_STATUS).keys()
        self.assertEqual(resp, True)

