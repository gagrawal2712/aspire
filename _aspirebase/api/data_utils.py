from django.contrib.auth.models import Group


class UserDataUtils:

    @staticmethod
    def get_user_groups(user_id):
        return list(set(list(Group.objects.filter(
            user=user_id).values_list('name', flat=True))))
