from django.db import models
from django.db.models.signals import m2m_changed
from django.shortcuts import get_object_or_404
from django.utils import timezone


class Team(models.Model):
    name = models.CharField("team name", max_length=20, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class User(models.Model):
    id = models.AutoField("id", primary_key=True)
    name = models.CharField("name", max_length=30)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.id} | {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in self.team.user_set.all():
            if user.name == self.name:
                for event in self.team.event_set.all():
                    Presence.objects.create(user=user, event=event)
                break


class ParentEvent(models.Model):
    name = models.CharField("parent event", max_length=20, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Event(models.Model):
    id = models.AutoField("id", primary_key=True)
    parent = models.ForeignKey(ParentEvent, on_delete=models.CASCADE, verbose_name="Parent Event")
    name = models.CharField("name", max_length=30, unique=True)
    participant = models.ManyToManyField(Team, blank=True)
    date = models.DateField("date", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id} | {self.name}"


def participant_changed(sender, **kwargs):
    event = kwargs["instance"]
    action = kwargs["action"]
    for id in kwargs['pk_set']:
        for user in Team.objects.get(pk=id).user_set.all():
            if action == "post_add":
                Presence.objects.create(user=user, event=event)
            elif action == "post_remove":
                Presence.objects.filter(user=user, event=event).delete()

m2m_changed.connect(participant_changed, sender=Event.participant.through)


class Presence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attend = models.BooleanField("Attendance", default=False)
    datetime = models.DateTimeField('datetime', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.id} | {self.user.name}"


def attend(user_id: int, event_id: int):
    user = get_object_or_404(User, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    if user.team not in event.participant.all():
        Event.objects.get_or_create(name=f"NOT INCLUDED {event.name}", parent=event.parent)
        event = Event.objects.get(name=f"NOT INCLUDED {event.name}")
        Presence.objects.create(user=user, event=event, attend=True, datetime=timezone.now())
        return "not_included"

    presence = Presence.objects.filter(user=user, event=event).first()
    presence.attend = True
    presence.datetime = timezone.now()
    presence.save()
    return "success"

def get_events():
    data = list()
    for event in Event.objects.order_by('-date', '-pk').all():
        data.append({
            'event_id'      : event.pk,
            'name'          : event.name,
            'date'          : event.date,
            'team_count'    : event.participant.count()
        })
    return data

def get_event_participant(event_id):
    data = list()
    event = Event.objects.get(pk=event_id)
    for presence in Presence.objects.filter(event=event).all():
        data.append({
            'user_id'   : presence.user.pk,
            'name'      : presence.user.name,
            'team'      : presence.user.team.name,
            'attend'    : presence.attend,
            'datetime'  : presence.datetime
        })
    return data