from .models import TeamMatch
import django_filters

class TeamMatchFilterSet(django_filters.FilterSet):
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    year = django_filters.NumberFilter(method='get_year', field_name='year')

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)
        return queryset

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)
        return queryset

    class Meta:
        model = TeamMatch
        fields = ['team']
