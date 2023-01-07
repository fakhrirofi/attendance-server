from django.contrib import admin
from .actions import export_as_xls, download_qr_code
from ..models import Competition, Event, Team, User, Presence

class ModelAdmin(admin.ModelAdmin):
    actions = [export_as_xls]

from . import competition, event, team, user, presence