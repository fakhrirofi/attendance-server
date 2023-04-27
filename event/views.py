import base64
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import RegistrationForm
from .models import Event, Presence
from .user_qr_code import encrypt, decrypt, get_event_ticket

def index(request):
    events = Event.objects.all()
    return render(request, 'event/index.html', {
        'events': events
    })

def registration(request, event_name):
    event = get_object_or_404(Event, name=event_name)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            presence = form.save(commit=False)
            presence.event = event
            presence.save()
            enc = encrypt(str(presence.pk))
            return HttpResponseRedirect(f"/event/registered/{enc}")
        else:
            HttpResponse("Form is invalid", 400)
    else:
        form = RegistrationForm()
    
    return render(request, 'event/registration.html', {
        'form': form,
        'event': event
    })

def registered(request, enc):
    enc_d = decrypt(enc)
    if enc_d == 'invalid':
        return HttpResponse("bad request", 400)
    presence = get_object_or_404(Presence, pk=int(enc_d))
    qr_code = get_event_ticket(enc, presence)
    return render(request, 'event/registered.html', {
        'qr_code' : base64.b64encode(qr_code).decode()
    })