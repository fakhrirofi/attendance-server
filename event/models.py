from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Event(models.Model):
    name = models.CharField("name", max_length=42)
    datetime = models.DateTimeField("date time")
    description = models.TextField()
    group_link = models.CharField(max_length=100)
    place = models.CharField(max_length=48)
    image = models.ImageField(upload_to="event_image")
    is_free = models.BooleanField("free registration")
    is_open = models.BooleanField("open registration")
    max_participant = models.IntegerField("max participant (optional)", blank=True, null=True)

    def __str__(self):
        return f"<Event {self.name}>"


class Presence(models.Model):
    name = models.CharField("name", max_length=48)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    institution = models.CharField(max_length=48)
    email = models.EmailField("email")
    phone_number = PhoneNumberField("Phone number (WhatsApp)", null=False, blank=False)
    proof_payment = models.ImageField("Proof of payment (image)", upload_to="payment", null=True)
    # proof payment is nullable to make it flexible
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
            'is_free'           : event.is_free,
            'is_open'           : event.is_open,
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
            'institution'           : presence.institution,
            'email'                 : presence.email,
            'payment_check'         : presence.payment_check,
            'attendance'            : presence.attendance,
            'datetime'              : presence.datetime,
        })
    return data