from django.urls import path
from aspireloan.api.views import LoanViewSet

urlpatterns = [

    path('create_loan/', LoanViewSet.as_view({
        'post': 'create_loan'}), name='create_loan'),

    path('update_loan_status/', LoanViewSet.as_view({
        'put': 'update_loan_status'}), name='update_loan_status'),

    path('list_user_loans/', LoanViewSet.as_view({
        'get': 'list_user_loans'}), name='list_user_loans'),

    path('loan_repayment/', LoanViewSet.as_view({
        'post': 'loan_repayment'}), name='loan_repayment'),

    path('get_loan_details/<int:loan_id>/', LoanViewSet.as_view({
        'get': 'get_loan_details'}), name='get_loan_details')
]