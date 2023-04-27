from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import RegistrationForm
from .models import Event
from .user_qr_code import get_encryption

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
            enc = get_encryption(presence).decode("utf-8")
            return HttpResponseRedirect(f"/event/registered/{enc}")
        else:
            # Whats happen when not valid?
            pass
    else:
        form = RegistrationForm()
    
    return render(request, 'event/registration.html', {
        'form': form,
        'event': event
    })

def registered(request, enc):
    return HttpResponse("Success")