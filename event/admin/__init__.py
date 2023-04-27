from django.contrib import admin
from ..models import Event, Presence

admin.site.register([Event, Presence])