from django.db import models
from django.utils import timezone

from aspireauth import crypto
from aspireauth.constants import TOKEN_TTL, CONSTANTS


class AuthTokenManager(models.Manager):

    def create(
            self, user, expires_on=TOKEN_TTL, ip_address=None,
            is_mobile=False, device_name=None, os_name=None, app_name="android",
            os_version=None, browser_name=None, browser_version=None):
        token = crypto.create_token_string()
        digest = crypto.hash_token(token)
        if expires_on is not None:
            expires_on = timezone.now() + expires_on
        instance = super(AuthTokenManager, self).create(
            token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH], digest=digest,
            user=user, expires_on=expires_on, ip_address=ip_address,
            device_name=device_name, is_mobile=is_mobile, os_name=os_name,
            os_version=os_version, browser_name=browser_name,
            browser_version=browser_version, app_name=app_name)
        return instance, token