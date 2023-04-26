from django.contrib.admin import SimpleListFilter
from . import ModelAdmin, admin, Presence


class CompetitionFilter(SimpleListFilter):
    title = 'competition'
    parameter_name = 'competition'

    def lookups(self, request, presence):
        competitions = set(p.event.competition for p in presence.model.objects.all())
        return [(c.id, c.name) for c in competitions]
    
    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset
        return queryset.filter(event__competition=self.value())


class PresenceAdmin(ModelAdmin):
    readonly_fields = ['user', 'event']
    fields = ['user', 'event', 'attend', 'datetime']
    list_display_links = ['user_name']
    list_display = ['user_id', 'user_name', 'team', 'competition', 'event_name', 'attend', 'datetime']
    list_filter = [CompetitionFilter, 'event']

    def user_id(self, obj):
        return str(obj.user.id).zfill(3)

    def user_name(self, obj):
        return obj.user.name
    
    def event_name(self, obj):
        return obj.event.name
    
    def competition(self, obj):
        return obj.event.competition.name

    def team(self, obj):
        return obj.user.team.name

admin.site.register(Presence, PresenceAdmin)