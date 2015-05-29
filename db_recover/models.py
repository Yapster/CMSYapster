from django.db import models
from admins.models import CmsUser
from announcements.models import Announcement
from chat.models import Conversation, Message
from groups.models import GroupPermission, Page
from contacts.models import Contact, List
from yap.models import Channel
from tasks.models import *
from cms_search_log.models import *
# from calendars.models import *
from wiki.models import *
from datetime import datetime
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
import django

class Recover(models.Model):
    """
    To rebuild the original database
    """
    @staticmethod
    def users():
        CmsUser.new_user(username="Chris", first_name="Chris", last_name="Lerus",
                         email="admin@admin.com", password="fefe")
        CmsUser.new_user(username="G", first_name="Gurkaran", last_name="Gulati",
                         email="g@yapsterapp.com", password="fefe")
        CmsUser.new_user(username="Abu", first_name="Abu", last_name="Ba",
                         email="abu@yapsterapp.com", password="fefe")
        CmsUser.new_user(username="Lilian", first_name="Lilian", last_name="Zu",
                         email="abu@yapsterapp.com", password="fefe")
        CmsUser.new_user(username="Tommy", first_name="Tommy", last_name="Sondgroth",
                         email="abu@yapsterapp.com", password="fefe")
        return

    @staticmethod
    def contacts():
        c = Contact.objects.create(firstname="Bill",
                                   lastname="Gates",
                                   email="boss@ms.com")
        c1 = Contact.objects.create(firstname="Nana",
                                    lastname="Mouskouri",
                                    phone="0102030405")
        return

    @staticmethod
    def group_permissions():
        group1 = GroupPermission.objects.create(group_name="Admin")
        group2 = GroupPermission.objects.create(group_name="Design")
        group3 = GroupPermission.objects.create(group_name="Frontend")
        group4 = GroupPermission.objects.create(group_name="Backend")
        group5 = GroupPermission.objects.create(group_name="Unix")
        group6 = GroupPermission.objects.create(group_name="UI")
        group7 = GroupPermission.objects.create(group_name="Mobile")
        p = Page.objects.create(name="groups permissions", url="/permissionsgroups/",
                                description="Manage permissions for groups")
        p2 = Page.objects.create(name="CmsUsers", url="/cmsusers/",
                                 description="Manage Cms users")
        p3 = Page.objects.create(name="Announcements", url="/announcements/",
                                 description="Manage Announcements")


        return

    @staticmethod
    def pages():
        return

    @staticmethod
    def conversations():

        return

    @staticmethod
    def groups():
        return

    @staticmethod
    def run():
        """
        Run all scripts
        """
        django.setup()

        group = GroupPermission.objects.create(group_name="No Group")
        group1 = GroupPermission.objects.create(group_name="Admin")
        group2 = GroupPermission.objects.create(group_name="Design/UI")
        group3 = GroupPermission.objects.create(group_name="Backend")
        group4 = GroupPermission.objects.create(group_name="Frontend")
        group5 = GroupPermission.objects.create(group_name="Mobile")

        user = CmsUser.new_user(username="Chris", first_name="Chris", last_name="Lerus",
                                email="chris@yapsterapp.com", password="fefe")
        user1 = CmsUser.new_user(username="Gurkaran", first_name="Gurkaran", last_name="Gulati",
                                 email="g@yapsterapp.com", password="fefe")
        user2 = CmsUser.new_user(username="Abu", first_name="Abu", last_name="Ba",
                                 email="abu@yapsterapp.com", password="fefe")
        user3 = CmsUser.new_user(username="Lilian", first_name="Lilian", last_name="Zhu",
                                 email="lilianz@yapsterapp.com", password="fefe")
        user4 = CmsUser.new_user(username="Tommy", first_name="Tommy", last_name="Sondgroth",
                                 email="tommy@yapsterapp.com", password="fefe")


        cmsuser = CmsUser.objects.get(username=user.username)
        cmsuser1 = CmsUser.objects.get(username=user1.username)
        cmsuser2 = CmsUser.objects.get(username=user2.username)
        cmsuser3 = CmsUser.objects.get(username=user3.username)
        cmsuser4 = CmsUser.objects.get(username=user4.username)

        # group1.members.add(cmsuser1)
        # group2.members.add(cmsuser3)
        # group2.members.add(cmsuser4)
        # group3.members.add(cmsuser)
        # group4.members.add(cmsuser2)
        # group5.members.add(cmsuser2)

        l = List.objects.create(name="Business Contacts",
                                description="Business guys who want to do business stuff",
                                created_by=user)

        l1 = List.objects.create(name="Fun Contacts",
                                 description="Fun guys who want to do fun stuff",
                                 created_by=user)

        l2 = List.objects.create(name="Admin Contacts",
                                 description="Only seen by the admin",
                                 created_by=user)


        p = Page.objects.create(name="groups permissions", url="/permissionsgroups/",
                            description="Manage permissions for groups")
        p2 = Page.objects.create(name="CmsUsers", url="/cmsusers/",
                            description="Manage Cms users")
        p3 = Page.objects.create(name="Announcements", url="/announcements/",
                             description="Manage Announcements")
        p4 = Page.objects.create(name="business_contacts_list", url="/contacts/lists/Business Contacts/",
                                 description="")
        p5 = Page.objects.create(name="fun_contacts_list", url="Fun Contacts",
                                 description="")
        p6 = Page.objects.create(name="admin_contacts_list", url="Admin Contacts",
                                 description="")

        p.perms.add(group1)

        p2.perms.add(group1)

        p3.perms.add(group1)

        p4.perms.add(group1)
        p4.perms.add(group2)
        p4.perms.add(group3)

        p5.perms.add(group1)
        p5.perms.add(group2)

        p6.perms.add(group1)

        c = Contact.objects.create(firstname="Bill",
                                   lastname="Gates",
                                   email="boss@ms.com")
        c1 = Contact.objects.create(firstname="Mark",
                                    lastname="Zuckzuck",
                                    email="boss@fb.com")
        c2 = Contact.objects.create(firstname="Nana",
                                    lastname="Mouskouri",
                                    phone="0102030405")
        c.lists.add(l)
        c.lists.add(l1)

        c1.lists.add(l)

        c2.lists.add(l2)

        c1 = Category.objects.create(name="Bug", color="0000FF", owner_category=user, is_public=True)
        c2 = Category.objects.create(name="Feature", color="00FF00", owner_category=user, is_public=True)
        c3 = Category.objects.create(name="Design", color="FF0000", owner_category=user, is_public=True)
        c4 = Category.objects.create(name="Brainstorming", color="FFFF00", owner_category=user, is_public=True)

        t1 = Task.objects.new_task(name="Bug IOS", description="Lorem ipsum dolor sit amet", category=c1, deadline=datetime(2014, 9, 3), priority=1, status='TO')
        t2 = Task.objects.new_task(name="New Tab Bar", description="Lorem ipsum dolor sit amet, ", category=c2, deadline=datetime(2014, 9, 2), priority=2, status='IP')
        t3 = Task.objects.new_task(name="Design Android", description="Lorem ipsum dolor sit amet, ", category=c3, deadline=datetime(2014, 9, 1), priority=3, status='DO')
        t4 = Task.objects.new_task(name="Think about Website", description="Lorem ipsum dolor sit amet, ", category=c4, deadline=datetime(2014, 8, 20), priority=4, status='TO')
        t5 = Task.objects.new_task(name="Bug CMS", description="Lorem ipsum dolor sit amet, ", category=c1, deadline=datetime(2014, 8, 22), priority=5, status='IP')
        t6 = Task.objects.new_task(name="Google Drive in CMS", description="Lorem ipsum dolor sit amet, ", category=c2, deadline=datetime(2014, 8, 24), priority=6, status='DO')



        t1.workers.add(user)
        t2.workers.add(user1)
        t3.workers.add(user2)
        t4.workers.add(user3)
        t5.workers.add(user1)
        t6.workers.add(user)
        t1.workers.add(user2)
        t1.workers.add(user3)
        t2.workers.add(user2)

        # Permissions :
        #
        # Group Manage
        # Users Manage
        # Contacts lists
        # Search
        # Calendar
        # Gits
        # Tasks
        # Announcements
        # Messenger
        # Databases
        # Servers
        # Stats
        # Channels


        for p in Permission.objects.all():
            p.delete()

        # New Perms
        content_type = ContentType.objects.get_for_model(User)
        permission1 = Permission.objects.create(codename='group_management',
                                                name='Manage Group',
                                                content_type=content_type)
        content_type = ContentType.objects.get_for_model(User)
        permission2 = Permission.objects.create(codename='users_management',
                                                name='Manage Users',
                                                content_type=content_type)
        content_type = ContentType.objects.get_for_model(CmsSearchLog)
        permission3 = Permission.objects.create(codename='search_management',
                                                name='Do Search',
                                                content_type=content_type)
        # content_type = ContentType.objects.get_for_model(MyCalendar)
        # permission4 = Permission.objects.create(codename='calendar_management',
        #                                         name='Has a calendar',
        #                                         content_type=content_type)
        content_type = ContentType.objects.get_for_model(User)
        permission5 = Permission.objects.create(codename='gits_management',
                                                name='Manage Gits',
                                                content_type=content_type)
        content_type = ContentType.objects.get_for_model(Task)
        permission6 = Permission.objects.create(codename='tasks_management',
                                                name='Has Tasks panel',
                                                content_type=content_type)
        content_type = ContentType.objects.get_for_model(Announcement)
        permission7 = Permission.objects.create(codename='announcement_management',
                                                name='Manage Announcement',
                                                content_type=content_type)
        content_type = ContentType.objects.get_for_model(Message)
        permission8 = Permission.objects.create(codename='messenger_access',
                                                name='Can Use Messenger',
                                                content_type=content_type)
        content_type = ContentType.objects.get_for_model(User)
        permission9 = Permission.objects.create(codename='amazon_databases_management',
                                                name='Amazon DB Management',
                                                content_type=content_type)
        content_type = ContentType.objects.get_for_model(User)
        permission10 = Permission.objects.create(codename='amazon_servers_management',
                                                 name='Amazon Servers Management',
                                                 content_type=content_type)
        content_type = ContentType.objects.get_for_model(User)
        permission11 = Permission.objects.create(codename='stats_management',
                                                 name='Stats management',
                                                 content_type=content_type)
        content_type = ContentType.objects.get_for_model(Channel)
        permission12 = Permission.objects.create(codename='channel_management',
                                                 name='Channel management',
                                                 content_type=content_type)

        # Create Group Perms
        group1 = Group.objects.create(name='Admin')
        group2 = Group.objects.create(name='Permanent')
        group3 = Group.objects.create(name='Intern')
        group4 = Group.objects.create(name='Extern')

        # Add Permissions to groups
        group1.permissions.add(permission1)
        group1.permissions.add(permission2)
        group1.permissions.add(permission3)
        # group1.permissions.add(permission4)
        group1.permissions.add(permission5)
        group1.permissions.add(permission6)
        group1.permissions.add(permission7)
        group1.permissions.add(permission8)
        group1.permissions.add(permission9)
        group1.permissions.add(permission10)
        group1.permissions.add(permission11)
        group1.permissions.add(permission12)

        group2.permissions.add(permission3)
        # group2.permissions.add(permission4)
        group2.permissions.add(permission5)
        group2.permissions.add(permission6)
        group2.permissions.add(permission7)
        group2.permissions.add(permission8)
        group2.permissions.add(permission9)
        group2.permissions.add(permission10)
        group2.permissions.add(permission11)
        group2.permissions.add(permission12)

        # group3.permissions.add(permission4)
        group3.permissions.add(permission6)
        group3.permissions.add(permission8)

        user.groups.add(group1)
        user1.groups.add(group2)
        user2.groups.add(group3)
        user3.groups.add(group4)

        t1 = WikiTag.objects.create(name="lol")
        t2 = WikiTag.objects.create(name="testing1234")
        t3 = WikiTag.objects.create(name="random")

        c1 = WikiCategory.objects.create(name="Design")
        c2 = WikiCategory.objects.create(name="Database")
        c3 = WikiCategory.objects.create(name="Server")

        p1 = WikiPage.objects.create(title="How The Database works", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua")
        p2 = WikiPage.objects.create(title="How The Design works", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua")
        p3 = WikiPage.objects.create(title="How The Server works", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua")

        p1.categories.add(c1)
        p2.categories.add(c1)
        p2.categories.add(c2)
        p2.categories.add(c3)
        p3.categories.add(c2)
        p3.categories.add(c3)

        p1.tags.add(t1)
        p1.tags.add(t2)
        p2.tags.add(t2)
        p1.tags.add(t3)
        p2.tags.add(t3)

        s1 = WikiSection.objects.create(order=1, title="Database Intro", page=p1, writer=user, content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        s2 = WikiSection.objects.create(order=2, title="Database Dev", page=p1, writer=user, content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        s3 = WikiSection.objects.create(order=3, title="Database End", page=p1, writer=user1, content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        s4 = WikiSection.objects.create(order=1, title="Design Intro", page=p2, writer=user1, content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        s5 = WikiSection.objects.create(order=2, title="Design Dev", page=p2, writer=user2, content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        s6 = WikiSection.objects.create(order=1, title="Server Intro", page=p3, writer=user3, content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        #
        p1.sections.add(s1)
        p1.sections.add(s2)
        p1.sections.add(s3)
        p2.sections.add(s4)
        p2.sections.add(s5)
        p3.sections.add(s6)

        WikiFolder.objects.create(name="No Folder", user=user)
        WikiFolder.objects.create(name="No Folder", user=user1)
        WikiFolder.objects.create(name="No Folder", user=user2)
        WikiFolder.objects.create(name="No Folder", user=user3)
        WikiFolder.objects.create(name="No Folder", user=user4)

        return