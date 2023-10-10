from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from aspireauth.auth import UserAuthTokenAuthentication


class TokenAuthViewSet(ViewSet):
    authentication_classes = (UserAuthTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    class Meta:
        abstract = True
