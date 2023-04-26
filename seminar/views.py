from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Event

from .forms import Registration

def index(request):
    events = Event.objects.all()
    return render(request, 'seminar/index.html', {
        'events': events
    })

def registration(request, event_name):
    event = get_object_or_404(Event, name=event_name)
    if request.method == 'POST':
        form = Registration(request.POST, request.FILES)
        if form.is_valid():
            presence = form.save(commit=False)
            presence.event = event
            presence.save()
            # CREATE QR CODE
            return HttpResponseRedirect("/seminar/")
    else:
        form = Registration()
    
    return render(request, 'seminar/registration.html', {
        'form': form,
        'event': event
    })

