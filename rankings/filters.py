from .models import TeamMatch
import django_filters

class TeamMatchFilterSet(django_filters.FilterSet):
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    event = django_filters.CharFilter(method='get_event', field_name='event')
    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('elo_end', 'elo'),
        ),
    )

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)
        return queryset

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)
        return queryset

    def get_event(self, queryset, field_name, value):
        if value: return queryset.filter(event=value)
        return queryset

    class Meta:
        model = TeamMatch
        fields = ['team', 'year', 'event']
