from . import admin, Presence, ModelAdmin
from . import export_as_xls, verify_registration, send_certificate_act

class PresenceAdmin(ModelAdmin):
    list_display_links = ['name']
    list_display = [
        'name', 'institution', 'email', 'phone_number',
        'proof_payment', 'payment_check', 'attendance', 'datetime'
    ]
    ordering = ['pk']
    search_fields = ['name', 'institution', 'email', 'phone_number']
    list_filter = ['event']
    actions = [export_as_xls, verify_registration, send_certificate_act]


admin.site.register(Presence, PresenceAdmin)