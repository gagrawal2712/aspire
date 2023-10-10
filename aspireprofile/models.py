from django.db import models
from django.contrib.auth.models import User

from _aspirebase.models import BaseModel
from aspireprofile.constants import GENDER_CHOICES


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    gender = models.CharField(
        max_length=2, null=True, blank=True, choices=GENDER_CHOICES)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=254, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone_country_code = models.CharField(
        default="+91", max_length=4, null=True, blank=True)

    # Default Models manager
    objects = models.Manager()

    def __str__(self):
        return "{} {} {}".format(self.user, self.phone, self.email)
