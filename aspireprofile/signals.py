from django.contrib.auth.models import User
from django.db.models.signals import post_save

from aspireprofile.models import Profile


def create_profile_on_user_create(sender, instance=None, **kwargs):
    if kwargs.get('created'):
        Profile.objects.get_or_create(user=instance)


post_save.connect(create_profile_on_user_create, sender=User)
