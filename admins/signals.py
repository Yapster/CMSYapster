from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from admins.models import CmsUser
from announcements.models import Announcement
from groups.models import GroupPermission, Page

@receiver(post_save, sender=CmsUser)
def mod_cmsuser(sender, instance, created, **kwargs):
    """
    Announcement or Notification when profile modified
    """
    if created:
        # TODO: New Profile => Notif all users?
        # TODO: S3 => Create new folder for pix
        return
    else:
        # TODO: Modification profile => Notif Admins?
        return


@receiver(post_save, sender=Announcement)
def new_announcement(sender, instance, created, **kwargs):
    if created:
        # TODO: Notif every user?
        return
    return

@receiver(post_save, sender=GroupPermission)
def new_group(sender, instance, created, selected_pages=None, **kwargs):
    return