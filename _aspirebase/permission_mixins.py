def check_group_allowed(user_groups, allowed_groups):
    return bool(set(allowed_groups).intersection(set(user_groups)))
