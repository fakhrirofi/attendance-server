from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Event(models.Model):
    name = models.CharField("name", max_length=30)
    datetime = models.DateTimeField("date time")
    max_participant = models.IntegerField("max participant", blank=True, null=True)

    def __str__(self):
        return f"<Event {self.name}>"


class Presence(models.Model):
    name = models.CharField("name", max_length=30)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    institution_origin = models.CharField("institution origin", max_length=30)
    email = models.EmailField("email")
    phone_number = PhoneNumberField(null=False, blank=False)
    proof_payment = models.ImageField(upload_to="payment")
    payment_check = models.BooleanField("payment check", default=False)
    attendance = models.BooleanField("attendance", default=False)
    datetime = models.DateTimeField("attendance time", blank=True, null=True)

    def __str__(self):
        return f"<Presence {self.event.name} | {self.name}>"


def attend(presence_id):
    presence = get_object_or_404(Presence, pk=presence_id)
    if not presence.payment_check:
        return "payment not checked"
    presence.attendance = True
    presence.datetime = timezone.now()
    presence.save()
    return "success"

def get_events():
    data = list()
    for event in Event.objects.order_by('-datetime').all():
        data.append({
            'id'                : event.pk,
            'name'              : event.name,
            'datetime'          : event.datetime,
            'registered'        : event.presence_set.count(),
            'max_participant'   : event.max_participant
        })
    return data

def get_event_presence(event_id):
    event = get_object_or_404(Event, pk=event_id)
    data = list()
    for presence in event.presence_set.all():
        data.append({
            'name'                  : presence.name,
            'institution_origin'    : presence.institution_origin,
            'email'                 : presence.email,
            'attendance'            : presence.attendance,
            'datetime'              : presence.datetime,
        })
    return data