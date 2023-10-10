from django.contrib.auth import get_user_model
from django.db import models

from _aspirebase.models import BaseModel
from aspireauth.constants import CONSTANTS
from aspireauth.managers import AuthTokenManager


# Create your models here.

class UserAuthToken(BaseModel):

    digest = models.CharField(
        max_length=CONSTANTS.DIGEST_LENGTH, unique=True)
    token_key = models.CharField(
        max_length=CONSTANTS.TOKEN_KEY_LENGTH, db_index=True)
    user = models.ForeignKey(
        get_user_model(), null=False, blank=False,
        related_name='auth_token_set', on_delete=models.CASCADE)
    is_mobile = models.BooleanField(default=False)
    device_name = models.CharField(max_length=255, null=True, blank=True)
    os_name = models.CharField(max_length=255, null=True, blank=True)
    os_version = models.CharField(max_length=255, null=True, blank=True)
    browser_name = models.CharField(max_length=255, null=True, blank=True)
    browser_version = models.CharField(max_length=255, null=True, blank=True)
    app_name = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    expires_on = models.DateTimeField(null=True, blank=True)

    objects = AuthTokenManager()

    def __str__(self):
        return '{} {}'.format(self.digest, self.user)