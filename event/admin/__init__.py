from django.contrib import admin
from .actions import export_as_xls
from ..models import Event, Presence

class ModelAdmin(admin.ModelAdmin):
    actions = [export_as_xls]

from . import event, presence