from admins.models import GroupPermission, CmsUser

def is_admin(user):
    if user:
        cmsuser = CmsUser.objects.get(user=user)
        return cmsuser.group.group_name == 'Admin'
    return False

def is_dev(user):
    if user:
        cmsuser = CmsUser.objects.get(user=user)
        return cmsuser.department == 'Dev'
    return False

def is_own_or_admin(user):
    if user:
        cmsuser = CmsUser.objects.get(user=user)
