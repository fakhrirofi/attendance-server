from . import admin, Presence, ModelAdmin
from . import export_as_xls, verify_registration

class PresenceAdmin(ModelAdmin):
    list_display_links = ['name']
    list_display = [
        'name', 'institution', 'email', 'phone_number',
        'proof_payment', 'payment_check', 'attendance', 'datetime'
    ]
    ordering = ['pk']
    list_filter = ['event']
    actions = [export_as_xls, verify_registration]


admin.site.register(Presence, PresenceAdmin)