# from admins.models import CmsUser
# from stats.models import Hashtag
# from groups.models import GroupPermission, Page
#
# GroupPermission.objects.create(group_name="Admin")
# GroupPermission.objects.create(group_name="Design")
# GroupPermission.objects.create(group_name="Python")
# GroupPermission.objects.create(group_name="Unix")
#
# group = GroupPermission.objects.get(pk=1)
# group2 = GroupPermission.objects.get(pk=2)
# CmsUser.new_user(username="chris", first_name="chris", last_name="lerus",
#                               email="admin@admin.com", password="fefe", group=group)
# Hashtag.objects.get_or_create(name="lol")
# GroupPermission.objects.create(group_name="No Group")
# p = Page.objects.create(name="groups permissions", url="/permissionsgroups/",
#                     description="Manage permissions for groups")
# p2 = Page.objects.create(name="CmsUsers", url="/cmsusers/",
#                     description="Manage Cms users")
# p3 = Page.objects.create(name="Announcements", url="/announcements/",
#                      description="Manage Announcements")
# p.perms.add(group)
# p.perms.add(group2)
# p2.perms.add(group)
# p3.perms.add(group)