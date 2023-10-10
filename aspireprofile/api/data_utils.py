from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from aspireauth.constants import TOKEN_TTL
from aspireauth.models import UserAuthToken


class ProfileDataUtils:

    @staticmethod
    def token_flow(
            user, user_agent=None, token_ttl=TOKEN_TTL, device_name=None,
            app_name="android", ip_address=None):
        # token_limit_per_app = get_token_limit(app_name)
        # if token_limit_per_app is not None:
        #     now = timezone.now()
        #     tokens = user.auth_token_set.filter(
        #         Q(expires_on__gt=now) | Q(expires_on__isnull=True)).filter(app_name=app_name)
        #     if tokens.count() >= token_limit_per_app:
        #         return None
        is_mobile = False
        device_name = device_name
        os_name = None
        os_version = None
        browser_name = None
        browser_version = None
        expires_on = None
        if token_ttl:
            expires_on = token_ttl + timezone.now()
        if user_agent:
            is_mobile = user_agent.is_mobile
            device_name = user_agent.device.family
            os_name = user_agent.os.family
            os_version = user_agent.os.version_string
            browser_name = user_agent.browser.family
            browser_version = user_agent.browser.version_string
            expires_on = expires_on
        f_dict = dict(
            user=user, is_mobile=is_mobile, device_name=device_name,
            os_name=os_name, os_version=os_version, browser_name=browser_name,
            browser_version=browser_version, app_name=app_name,
            ip_address=ip_address)
        try:
            existing_token = UserAuthToken.objects.get(**f_dict)
            existing_token.delete()
        except UserAuthToken.DoesNotExist:
            pass
        except UserAuthToken.MultipleObjectsReturned:
            UserAuthToken.objects.filter(**f_dict).delete()
        instance, token = UserAuthToken.objects.create(
            user, is_mobile=is_mobile, device_name=device_name, os_name=os_name,
            os_version=os_version, ip_address=ip_address,
            browser_name=browser_name, browser_version=browser_version,
            expires_on=expires_on, app_name=app_name)
        return token

    @staticmethod
    def get_profile(u_name):
        profile = None
        try:
            user = User.objects.get(username=u_name)
            try:
                profile = user.profile
            except ObjectDoesNotExist:
                pass
        except User.DoesNotExist:
            pass
        return profile

    def map_to_data_dict(self, token, profile):
        return dict(
            is_active=profile.user.is_active,
            token=token if token else None,
            user_data=self.get_user_data(profile))

    @staticmethod
    def get_user_data(profile):
        return {
            "name": profile.full_name,
            "email": profile.email,
            "phone": profile.phone,
            "gender": profile.gender,
            "dob": profile.dob,
            "country_code": profile.phone_country_code,
            "user_id": profile.user_id,
            "added_on": profile.created_at,
            "is_superuser": profile.user.is_superuser,
            "username": profile.user.username
        }