from . import admin, User, Team, ModelAdmin

class UserInLine(admin.TabularInline):
    model = User
    fields = ['name']
    extra = 0

class TeamAdmin(ModelAdmin):
    list_display = ['name', 'competitions', 'members']
    fields = ['name']
    inlines = [UserInLine]

    def members(self, obj):
        return obj.user_set.count()

    def competitions(self, obj):
        return ", ".join([c.name for c in obj.competition_set.all()])

admin.site.register(Team, TeamAdmin)