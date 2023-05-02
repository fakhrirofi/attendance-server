from . import admin, Event, ModelAdmin


class EventAdmin(ModelAdmin):
    list_display_links = ['name']
    list_display = [
        'name', 'datetime', 'place', 'is_free', 'is_open', 'registered', 
    ]
    ordering = ['pk']

    def registered(self, obj):
        return obj.presence_set.count()


admin.site.register(Event, EventAdmin)