from django.db import models
from admins.models import User, CmsUser
from announcements.models import Announcement
from chat.models import Conversation, Message
from groups.models import GroupPermission, Page
from contacts.models import Contact, List

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

        group1.members.add(cmsuser1)
        group2.members.add(cmsuser3)
        group2.members.add(cmsuser4)
        group3.members.add(cmsuser)
        group4.members.add(cmsuser2)
        group5.members.add(cmsuser2)

        l = List.objects.create(name="Business Contacts",
                            description="Business guys who want to do business stuff",
                            created_by=user)

        l1 = List.objects.create(name="Fun Contacts",
                            description="Fun guys who want to do fun stuff",
                            created_by=user)

        l2 = List.objects.create(name="Admin Contacts",
                            description="Only seen by the admin",
                            created_by=user)

        l.groups.add(group2)
        l.groups.add(group3)

        l1.groups.add(group2)
        l1.groups.add(group3)
        l1.groups.add(group4)
        l1.groups.add(group5)

        l2.groups.add(group1)

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

        return