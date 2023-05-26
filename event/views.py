import base64
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from urllib.parse import unquote

from .forms import RegistrationForm, RegistrationFormFree
from .models import Event, Presence
from .user_qr_code import encrypt, decrypt, get_event_ticket

def index(request):
    events = Event.objects.all()
    return render(request, 'event/index.html', {
        'events': events
    })

def registration(request, event_name):
    event = get_object_or_404(Event, name=unquote(event_name))
    if not event.is_open:
        return HttpResponseRedirect("/")
    if event.max_participant != None:
        if event.presence_set.count() >= event.max_participant:
            event.is_open = False
            event.save()
            return HttpResponseRedirect("/")
    if request.method == 'POST':
        if event.is_free:
            form = RegistrationFormFree(request.POST, request.FILES)
        else:
            form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            presence = form.save(commit=False)
            presence.event = event
            presence.save()
# WARNING: edited due to prevent email to send as spam
            # if event.is_free :
                # presence.payment_check = True
                # presence.save()
            enc = encrypt(str(presence.pk))
            return HttpResponseRedirect(f'/registered/{enc}')
            # else:
            #     return render(request, 'event/under_review.html')
        else:
            HttpResponse("form invalid", 400)
    else:
        if event.is_free:
            form = RegistrationFormFree()
        else:
            form = RegistrationForm()
    
    return render(request, 'event/registration.html', {
        'form': form,
        'event': event
    })

def registered(request, enc):
    enc_d = decrypt(enc)
    if enc_d == "invalid":
        return HttpResponse("bad request", 400)
    presence = get_object_or_404(Presence, pk=int(enc_d))
    qr_code = get_event_ticket(enc, presence)
    return render(request, 'event/registered.html', {
        'qr_code' : base64.b64encode(qr_code).decode(),
        'group_link' : presence.event.group_link,
        'filename' : presence.event.name + "_" + presence.name
    })