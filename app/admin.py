from django.contrib import admin
from .models import *

admin.site.register([Team, User, Event, Presence])
