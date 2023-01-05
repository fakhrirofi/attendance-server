from django.db import models
from django.db.models.signals import m2m_changed
from django.shortcuts import get_object_or_404
from django.utils import timezone


class Team(models.Model):
    name = models.CharField("team name", max_length=20, unique=True)

    def __str__(self) -> str:
        return f"<Team {self.name}>"


class User(models.Model):
    user_id = models.IntegerField("user id", primary_key=True, unique=True)
    name = models.CharField("name", max_length=30)
    team = models.ForeignKey(Team, blank=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"<User {self.name}>"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user = None
        for user in self.team.user_set.all():
            if user.name == self.name:
                user = user
                break
        for event in self.team.event_set.all():
            Presence.objects.create(user=user, event=event)


class Event(models.Model):
    event_id = models.IntegerField("event id", primary_key=True, unique=True)
    name = models.CharField("event name", max_length=30, unique=True)
    participant = models.ManyToManyField(Team)
    date = models.DateField("date", null=True)

    def __str__(self) -> str:
        return f"<Event {self.name}>"


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
    datetime = models.DateTimeField('datetime', null=True)

    def __str__(self) -> str:
        return f"<Presence {self.user.name} on {self.event.name}>"


def attend(user_id: int, event_id: int):
    user = get_object_or_404(User, user_id=user_id)
    event = get_object_or_404(Event, event_id=event_id)
    if user.team not in event.participant.all():
        Event.objects.get_or_create(name=f"NOT INCLUDED {event.name}")
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
    for event in Event.objects.order_by('-date', '-event_id').all():
        data.append({
            'event_id'      : event.event_id,
            'name'          : event.name,
            'date'          : event.date,
            'team_count'    : event.participant.count()
        })
    return data

def get_event_participant(event_id):
    data = list()
    event = Event.objects.get(event_id=event_id)
    for presence in Presence.objects.filter(event=event).all():
        data.append({
            'name'      : presence.user.name,
            'team'      : presence.user.team.name,
            'attend'    : presence.attend,
            'datetime'  : presence.datetime
        })
    return data