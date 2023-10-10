import binascii

from django.db import DatabaseError
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header)

from aspireauth.constants import (
    AUTH_HEADER_PREFIX, CONSTANTS, AUTO_REFRESH, TOKEN_TTL,
    MIN_REFRESH_INTERVAL, LOGIN_REFRESH_INTERVAL)
from aspireauth.crypto import hash_token
from aspireauth.models import UserAuthToken
from aspireauth.signals import token_expired

try:
    from hmac import compare_digest
except ImportError:
    def compare_digest(a, b):
        return a == b


class UserAuthTokenAuthentication(BaseAuthentication):
    """
    This authentication scheme uses Knox AuthTokens for authentication.
    Similar to DRF TokenAuthentication, it overrides a large amount of that
    authentication scheme to cope with the fact that Tokens are not stored
    in plaintext in the database
    If successful
    - `request.user` will be a django `User` instance
    - `request.auth` will be an `AuthToken` instance
    """
    model = UserAuthToken

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        prefix = AUTH_HEADER_PREFIX.encode()
        if not auth:
            return None
        if auth[0].lower() != prefix.lower():
            # Authorization header is possibly for another backend
            return None
        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                detail='You are not allowed to perform this operation')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(
                detail='Invalid Token, key should not contained spaces')
        user, auth_token = self.authenticate_credentials(auth[1], request.META)
        return user, auth_token

    def authenticate_credentials(self, token, meta):
        """
        :param token:
        :param meta:
        :return: Due to the random nature of hashing a value, this must inspect
        each auth_token individually to find the correct one.
        Tokens that have expired will be deleted and skipped
        """
        msg = 'Invalid token.'
        token = token.decode("utf-8")
        for auth_token in UserAuthToken.objects.filter(
                token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH]):
            if self._cleanup_token(auth_token):
                continue
            try:
                digest = hash_token(token)
            except (TypeError, binascii.Error):
                raise exceptions.AuthenticationFailed(detail=msg)
            if compare_digest(digest, auth_token.digest):
                if AUTO_REFRESH and auth_token.expires_on:
                    self.renew_token(auth_token)
                return self.validate_user(auth_token, meta)
        raise exceptions.AuthenticationFailed(detail=msg)

    @staticmethod
    def renew_token(auth_token):
        current_expiry = auth_token.expires_on
        new_expiry = timezone.now() + TOKEN_TTL
        auth_token.expires_on = new_expiry
        # Throttle refreshing of token to avoid db writes
        delta = (new_expiry - current_expiry).total_seconds()
        if delta > MIN_REFRESH_INTERVAL:
            auth_token.save(update_fields=('expires_on',))

    def validate_user(self, auth_token, meta):
        if not auth_token.user.is_active:
            raise exceptions.AuthenticationFailed(
                detail='User inactive or deleted.')
        delta = (timezone.now() - auth_token.updated_at).total_seconds()
        if delta > LOGIN_REFRESH_INTERVAL:
            try:
                auth_token.ip_address = self.get_client_ip(meta)
                auth_token.save(update_fields=('updated_at', 'ip_address'))
            except DatabaseError:
                pass
        return auth_token.user, auth_token

    @staticmethod
    def get_client_ip(meta):
        x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = meta.get('REMOTE_ADDR')
        return ip

    def authenticate_header(self, request):
        return AUTH_HEADER_PREFIX

    def _cleanup_token(self, auth_token):
        for other_token in auth_token.user.auth_token_set.all():
            if other_token.digest != auth_token.digest and (
                    other_token.expires_on):
                if other_token.expires_on < timezone.now():
                    other_token.delete()
                    username = other_token.user.get_username()
                    token_expired.send(
                        sender=self.__class__,
                        username=username, source="other_token")
        if auth_token.expires_on is not None:
            if auth_token.expires_on < timezone.now():
                username = auth_token.user.get_username()
                auth_token.delete()
                token_expired.send(
                    sender=self.__class__,
                    username=username, source="auth_token")
                return True
        return False
