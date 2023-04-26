from . import admin, Event, ModelAdmin, Competition


class EventInLine(admin.TabularInline):
    model = Event
    fields = ['name', 'date']
    extra = 0
    ordering = ['date', 'id']

class CompetitionAdmin(ModelAdmin):
    fields = ['name', 'teams']
    inlines = [EventInLine]
    list_display = ['name', 'events', 'team_count', 'participant']

    def events(self, obj):
        return obj.event_set.count()
    
    def team_count(self, obj):
        return obj.teams.count()

    def participant(self, obj):
        total = 0
        for team in obj.teams.all():
            total += team.user_set.count()
        return total

admin.site.register(Competition, CompetitionAdmin)