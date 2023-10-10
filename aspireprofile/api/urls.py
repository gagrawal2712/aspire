from django.urls import path
from aspireprofile.api.views import ProfileSignUpAndLoginViewSet

urlpatterns = [

    path('username_login/', ProfileSignUpAndLoginViewSet.as_view({
        'put': 'username_login'}), name='username_login')
]