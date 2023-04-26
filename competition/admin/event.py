from . import admin, Presence, ModelAdmin, Event

class PresenceInLine(admin.TabularInline):
    model = Presence
    extra = 0
    readonly_fields = ['id', 'name']
    fields = ['id', 'name', 'attend', 'datetime']

    def name(self, obj):
        return obj.user.name

    def id(self, obj):
        return obj.user.id

class EventAdmin(ModelAdmin):
    list_display_links = ['name']
    list_display = ['name', 'competition', 'date', 'attendances', 'participant']
    fields = ['competition', 'name', 'date']
    inlines = [PresenceInLine]
    ordering = ['id']
    list_filter = ['competition']

    def participant(self, obj):
        total = 0
        for team in obj.competition.teams.all():
            total += team.user_set.count()
        return total
    
    def attendances(self, obj):
        total = 0
        for presence in Presence.objects.filter(event=obj):
            if presence.attend:
                total += 1
        return total

admin.site.register(Event, EventAdmin)