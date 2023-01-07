from django.contrib.admin import SimpleListFilter
from . import ModelAdmin, User, admin, export_as_xls, download_qr_code, Competition


class CompetitionFilter(SimpleListFilter):
    title = 'competition'
    parameter_name = 'competition'

    def lookups(self, request, user):
        competitions = Competition.objects.all()
        return [(c.id, c.name) for c in competitions]
    
    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset
        teams = Competition.objects.get(pk=self.value()).teams.all()
        return queryset.filter(team__in=teams)


class UserAdmin(ModelAdmin):
    list_display_links = ['name']
    list_display = ['user_id', 'name', 'team', 'competitions']
    fields = ['name', 'team']
    ordering = ['id']
    actions = [export_as_xls, download_qr_code]
    list_filter = [CompetitionFilter, 'team']

    def user_id(self, obj):
        return str(obj.id).zfill(3)

    def competitions(self, obj):
        return ", ".join([c.name for c in obj.team.competition_set.all()])

admin.site.register(User, UserAdmin)