from django.contrib import admin
from .models import ParentEvent, Event, Team, User, Presence
from .actions import export_as_xls

class ModelAdmin(admin.ModelAdmin):
    actions = [export_as_xls]

# PARENT EVENT
class EventInLine(admin.TabularInline):
    model = Event
    fields = ['name', 'date']
    extra = 0
    ordering = ['date', 'id']

class ParentEventAdmin(ModelAdmin):
    fields = ['name']
    inlines = [EventInLine]
    list_display = ['name', 'events', 'teams', 'attendances','total_registered']

    def events(self, obj):
        return obj.event_set.count()
    
    def teams(self, obj):
        total = 0
        for event in obj.event_set.all():
            total += event.participant.count()
        return total

    def attendances(self, obj):
        total = 0
        for presence in Presence.objects.all():
            if presence.attend:
                total += 1
        return total

    def total_registered(self, obj):
        total = 0
        for event in obj.event_set.all():
            for team in event.participant.all():
                total += team.user_set.count()
        return total

admin.site.register(ParentEvent, ParentEventAdmin)

# EVENT
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
    list_display = ['id', 'name', 'date', 'teams', 'attendances', 'total_registered']
    fields = ['parent', 'name', 'date', 'participant']
    inlines = [PresenceInLine]
    ordering = ['id']

    def total_registered(self, obj):
        total = 0
        for team in obj.participant.all():
            total += team.user_set.count()
        return total
    
    def attendances(self, obj):
        total = 0
        for presence in Presence.objects.filter(event=obj):
            if presence.attend:
                total += 1
        return total
    
    def teams(self, obj):
        return obj.participant.count()

admin.site.register(Event, EventAdmin)

# TEAM
class UserInLine(admin.TabularInline):
    model = User
    fields = ['name']
    extra = 0

class TeamAdmin(ModelAdmin):
    list_display = ['name', 'members']
    fields = ['name']
    inlines = [UserInLine]

    def members(self, obj):
        return obj.user_set.count()

admin.site.register(Team, TeamAdmin)

# USER
class UserAdmin(ModelAdmin):
    list_display_links = ['name']
    list_display = ['id', 'name', 'team']
    fields = ['name', 'team']
    ordering = ['id']

admin.site.register(User, UserAdmin)

# PRESENCE
class PresenceAdmin(ModelAdmin):
    readonly_fields = ['user', 'event']
    fields = ['user', 'event', 'attend', 'datetime']
    list_display_links = ['user_name']
    list_display = ['user_id', 'user_name', 'event_name', 'attend', 'datetime']
    list_filter = ['event']

    def user_name(self, obj):
        return obj.user.name
    
    def event_name(self, obj):
        return obj.event.name


admin.site.register(Presence, PresenceAdmin)
