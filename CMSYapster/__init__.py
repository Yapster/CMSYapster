# from admins.models import GroupPermission, CmsUser
# from stats.models import Hashtag
#
# GroupPermission.objects.create(group_name="Admin")
# GroupPermission.objects.create(group_name="Design")
# GroupPermission.objects.create(group_name="Python")
# GroupPermission.objects.create(group_name="Unix")
#
# group = GroupPermission.objects.get(pk=1)
# CmsUser.objects.get_or_create(username="chris", firstname="chris", lastname="lerus",
#                               email="admin@admin.com", password="fefe", group=group)
# Hashtag.objects.get_or_create(name="lol")