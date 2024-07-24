
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from ..authorize.models import *
from .models import *

## UTILS ##

def manage_calendar(cls):
    """Connects handlers for calendar management."""
    post_save.connect(create_calendar, sender=cls)
    post_delete.connect(delete_calendar, sender=cls)

## HANDLERS ##

@receiver(m2m_changed, sender=Event.attendees.through)
def update_attendees_event_permissions(sender, instance, action, **kwargs):
    """Updates the permissions assigned to the attendees of the given event."""
    if action in ["post_add", "post_remove", "post_clear"]:
        can_view_this_event, _ = ObjectPermission.objects.get_or_create_by_natural_key("view_event", "calendar", "event", instance.pk)
        can_change_this_event, _ = ObjectPermission.objects.get_or_create_by_natural_key("change_event", "calendar", "event", instance.pk)

        for att in instance.attendees.all():
            can_view_this_event.users.add(att)
            can_change_this_event.users.add(att)

@receiver(post_save, sender=Event)
def create_calendar(sender, instance, created, **kwargs):
    """Updates the calendar field of the object's stream."""
    if created and hasattr(instance, "calendar") and not instance.calendar:
        calendar, is_new = Calendar.objects.get_or_create(
            title=f"{instance}'s calendar",
            slug=f"{sender.__name__.lower()}_{instance.pk}_calendar",
            description=_("Calendar for %s") % instance
        )
        if not is_new:
            for e in calendar.events.all():
                e.delete()
        instance.calendar = calendar
        instance.save()

@receiver(post_delete, sender=Event)
def delete_calendar(sender, instance, **kwargs):
    """Deletes the calendar of the given object."""
    calendar = instance.calendar
    if calendar:
        calendar.delete()
        instance.calendar = None

## CONNECTIONS ##

"""
post_save.connect(update_author_permissions, sender=Event, dispatch_uid="update_event_permissions")
m2m_changed.connect(update_attendees_event_permissions, sender=Event.attendees.through, dispatch_uid="update_event_permissions")

post_save.connect(notify_object_created, sender=Event, dispatch_uid="event_created")
post_save.connect(notify_object_changed, sender=Event, dispatch_uid="event_changed")
post_delete.connect(notify_object_deleted, sender=Event, dispatch_uid="event_deleted")

m2m_changed.connect(notify_m2m_changed, sender=Event.attendees.through, dispatch_uid="attendees_changed")

manage_stream(Event)
make_observable(Event)

manage_calendar(UserProfile)
"""
