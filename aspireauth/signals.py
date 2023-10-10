import django.dispatch
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete

from aspireauth.models import UserAuthToken

token_expired = django.dispatch.Signal()


def clean_token_on_user_inactive(sender, instance=None, **kwargs):
    if isinstance(instance, User) and hasattr(instance, "id"):
        if not instance.is_active:
            UserAuthToken.objects.filter(user_id=instance.id).delete()


post_save.connect(clean_token_on_user_inactive, sender=User)
