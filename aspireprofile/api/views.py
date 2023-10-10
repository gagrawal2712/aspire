from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from aspireprofile.api.utils import ProfileViewUtils


class ProfileSignUpAndLoginViewSet(ViewSet):
    view_class = ProfileViewUtils()

    def username_login(self, request):
        resp, status_code = self.view_class.username_login(request)
        return Response(resp, status=status_code)