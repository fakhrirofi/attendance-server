from . import admin, Presence, ModelAdmin


class PresenceAdmin(ModelAdmin):
    list_display_links = ['name']
    list_display = [
        'name', 'institution', 'email', 'phone_number',
        'proof_payment', 'payment_check', 'attendance', 'datetime'
    ]
    ordering = ['pk']
    list_filter = ['event']


admin.site.register(Presence, PresenceAdmin)