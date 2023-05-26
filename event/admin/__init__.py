from django.contrib import admin
from .actions import export_as_xls, verify_registration, send_certificate_act, send_certificate
from ..models import Event, Presence

class ModelAdmin(admin.ModelAdmin):
    actions = [export_as_xls]

from . import event, presence