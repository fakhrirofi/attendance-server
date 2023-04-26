from django.db import models
from django.db.models.signals import m2m_changed
from django.shortcuts import get_object_or_404
from django.utils import timezone


class Team(models.Model):
    name = models.CharField("name", max_length=20)

    def __str__(self) -> str:
        return f"{self.name}"


class Competition(models.Model):
    name = models.CharField("name", max_length=20, unique=True)
    teams = models.ManyToManyField(Team, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"


def auto_register_member(sender, **kwargs):
    events = kwargs["instance"].event_set.all()
    action = kwargs["action"]
    for id in kwargs['pk_set']:
        for user in Team.objects.get(pk=id).user_set.all():
            for event in events:
                if "NOT INCLUDED" in event.name:
                    continue
                if action == "post_add":
                    Presence.objects.create(user=user, event=event)
                elif action == "post_remove":
                    Presence.objects.filter(user=user, event=event).delete()

m2m_changed.connect(auto_register_member, Competition.teams.through)


class User(models.Model):
    id = models.AutoField("id", primary_key=True)
    name = models.CharField("name", max_length=30)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.id} | {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for competition in self.team.competition_set.all():
            for event in competition.event_set.all():
                Presence.objects.create(user=self, event=event)


class Event(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name="competition")
    name = models.CharField("name", max_length=30)
    date = models.DateField("date", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.competition.name} | {self.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for team in self.competition.teams.all():
            for user in team.user_set.all():
                Presence.objects.create(user=user, event=self)


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

    if event.competition not in user.team.competition_set.all():
        Competition.objects.get_or_create(name="Global Event")
        competition = Competition.objects.get(name="Global Event")
        Event.objects.get_or_create(name=f"NOT INCLUDED {event.name}", competition=competition)
        event = Event.objects.get(name=f"NOT INCLUDED {event.name}")
        Presence.objects.create(user=user, event=event, attend=True, datetime=timezone.now())
        return "not_included"

    presence = Presence.objects.filter(user=user, event=event).first()
    presence.attend = True
    presence.datetime = timezone.now()
    presence.save()
    return "success"

def get_competition():
    data = list()
    for competition in Competition.objects.order_by('name').all():
        data.append({
            'competition_id'    : competition.pk,
            'name'              : competition.name,
            'teams'             : competition.teams.count()
        })
        return data

def get_event(competition_id: int):
    data = list()
    for event in Competition.objects.get(pk=competition_id).event_set.order_by('date', 'pk').all():
        data.append({
            'event_id'      : event.pk,
            'name'          : event.name,
            'date'          : event.date,
        })
    return data

def get_event_presence(event_id: int):
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