from django.contrib import admin

from aspireprofile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'active',
        'gender',
        'full_name',
        'phone',
        'phone_country_code',
        'email',
        'dob',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'active',
        'dob'
    )
    search_fields = ("full_name", 'phone')
    date_hierarchy = 'created_at'
