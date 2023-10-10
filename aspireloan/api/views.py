from rest_framework.response import Response

from _aspirebase.api.views import TokenAuthViewSet
from aspireloan.api.utils import LoanUtils


class LoanViewSet(TokenAuthViewSet):
    loan_utils = LoanUtils()

    def create_loan(self, request):
        resp, status_code = self.loan_utils.create_loan(
            request.user, **request.data)
        return Response(resp, status=status_code)

    def update_loan_status(self, request):
        resp, status_code = self.loan_utils.update_loan_status(
            request.user, **request.data)
        return Response(resp, status=status_code)

    def list_user_loans(self, request):
        resp, status_code = self.loan_utils.list_user_loans(
            request.user, **request.query_params.dict())
        return Response(resp, status=status_code)

    def loan_repayment(self, request):
        resp, status_code = self.loan_utils.loan_repayment(**request.data)
        return Response(resp, status=status_code)

    def get_loan_details(self, request, loan_id):
        resp, status_code = self.loan_utils.get_loan_details(request.user, loan_id)
        return Response(resp, status=status_code)
