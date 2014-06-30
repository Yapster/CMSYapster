# from admins.models import CmsUser
# from stats.models import Hashtag
# from groups.models import GroupPermission, Page
# from contacts.models import Contact, List, Note
# from django.contrib.auth.models import User
# from chat.models import Conversation, Message
# from admins.models import Profile
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
# CmsUser.new_user(username="G", first_name="Gurkaran", last_name="Gulati",
#                                email="g@yapsterapp.com", password="fefe", group=group)
# CmsUser.new_user(username="Abu", first_name="Abu", last_name="Ba",
#                                email="abu@yapsterapp.com", password="fefe", group=group2)
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
# cmsuser = CmsUser.objects.get(pk=1)
# cmsuser2 = CmsUser.objects.get(pk=2)
# user = User.objects.get(username=cmsuser.username)
# user2 = User.objects.get(username=cmsuser2.username)
# l = List.objects.create(name="Business Contacts",
#                     description="Business guys who want to do business stuff",
#                     created_by=user)
# l.groups.add(group)
# l1 = List.objects.create(name="Fun Contacts",
#                     description="Fun guys who want to do fun stuff",
#                     created_by=user)
# l1.groups.add(group)
# l1.groups.add(group2)
# c = Contact.objects.create(firstname="Bill",
#                            lastname="Gates",
#                            email="boss@ms.com")
# c.lists.add(l)
# c.lists.add(l1)
# c1 = Contact.objects.create(firstname="Nana",
#                             lastname="Mouskouri",
#                             phone="0102030405")
# c1.lists.add(l)
# c1.lists.add(l1)
# conv = Conversation.objects.create()
#
# conv.users.add(user)
# conv.users.add(user2)
#
# Profile.objects.create(user=user, description="This is a test")