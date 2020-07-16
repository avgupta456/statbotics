import django_filters

from .models import (
    Year,
    Team,
    TeamYear,
    Event,
    TeamEvent,
    Match,
    TeamMatch
)


class YearFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='get_year', field_name='year')

    o = django_filters.OrderingFilter(
        fields=(
            ('elo_acc', 'elo_acc'),
            ('elo_mse', 'elo_mse'),
            ('opr_acc', 'opr_acc'),
            ('opr_mse', 'opr_mse'),
            ('mix_acc', 'mix_acc'),
            ('mix_mse', 'mix_mse'),
        ),
    )

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)  # noqa 701
        return queryset

    class Meta:
        model = Year
        fields = ['year']


class TeamFilterSet(django_filters.FilterSet):
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    active = django_filters.NumberFilter(method='get_active', field_name='active')  # noqa 502
    state = django_filters.CharFilter(method='get_state', field_name='state')
    country = django_filters.CharFilter(method='get_country', field_name='country')  # noqa 502
    district = django_filters.CharFilter(method='get_district', field_name='district')  # noqa 502

    o = django_filters.OrderingFilter(
        fields=(
            ('team', 'team'),
            ('elo', 'elo'),
            ('elo_recent', 'elo_recent'),
            ('elo_mean', 'elo_mean'),
            ('elo_max', 'elo_max'),
        ),
    )

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)  # noqa 701
        return queryset

    def get_active(self, queryset, field_name, value):
        if value: return queryset.filter(active=value)  # noqa 701
        return queryset

    def get_state(self, queryset, field_name, value):
        if value: return queryset.filter(state=value)  # noqa 701
        return queryset

    def get_country(self, queryset, field_name, value):
        if value: return queryset.filter(country=value)  # noqa 701
        return queryset

    def get_district(self, queryset, field_name, value):
        if value: return queryset.filter(district=value)  # noqa 701
        return queryset

    class Meta:
        model = Team
        fields = ['team', 'active', 'state', 'country',  'district']


class TeamYearFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    state = django_filters.CharFilter(method='get_state', field_name='state')
    country = django_filters.CharFilter(method='get_country', field_name='country')  # noqa 502
    district = django_filters.CharFilter(method='get_district', field_name='district')  # noqa 502

    o = django_filters.OrderingFilter(
        fields=(
            ('year', 'year'),
            ('team', 'team'),
            ('elo_start', 'elo_start'),
            ('elo_pre_champs', 'elo_pre_champs'),
            ('elo_end', 'elo_end'),
            ('elo_mean', 'elo_mean'),
            ('elo_max', 'elo_max'),
        ),
    )

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)  # noqa 701
        return queryset

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)  # noqa 701
        return queryset

    def get_state(self, queryset, field_name, value):
        if value: return queryset.filter(state=value)  # noqa 701
        return queryset

    def get_country(self, queryset, field_name, value):
        if value: return queryset.filter(country=value)  # noqa 701
        return queryset

    def get_district(self, queryset, field_name, value):
        if value: return queryset.filter(district=value)  # noqa 701
        return queryset

    class Meta:
        model = TeamYear
        fields = ['year', 'team', 'state', 'country', 'district']


class EventFilterSet(django_filters.FilterSet):
    event = django_filters.CharFilter(method='get_event', field_name='event')
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    state = django_filters.CharFilter(method='get_state', field_name='state')
    country = django_filters.CharFilter(method='get_country', field_name='country')  # noqa 502
    district = django_filters.CharFilter(method='get_district', field_name='district')  # noqa 502
    type = django_filters.NumberFilter(method='get_type', field_name='type')
    week = django_filters.NumberFilter(method='get_week', field_name='week')

    o = django_filters.OrderingFilter(
        fields=(
            ('year', 'year'),
            ('elo_top8', 'elo_top8'),
            ('elo_top24', 'elo_top24'),
            ('elo_mean', 'elo_mean'),
        ),
    )

    def get_event(self, queryset, field_name, value):
        if value: return queryset.filter(event=value)  # noqa 701
        return queryset

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)  # noqa 701
        return queryset

    def get_state(self, queryset, field_name, value):
        if value: return queryset.filter(state=value)  # noqa 701
        return queryset

    def get_country(self, queryset, field_name, value):
        if value: return queryset.filter(country=value)  # noqa 701
        return queryset

    def get_district(self, queryset, field_name, value):
        if value: return queryset.filter(district=value)  # noqa 701
        return queryset

    def get_type(self, queryset, field_name, value):
        if value: return queryset.filter(type=value)  # noqa 701
        return queryset

    def get_week(self, queryset, field_name, value):
        if value: return queryset.filter(week=value)  # noqa 701
        return queryset

    class Meta:
        model = Event
        fields = ['event', 'year', 'country', 'state', 'district',
                  'type', 'week']


class TeamEventFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    event = django_filters.CharFilter(method='get_event', field_name='event')
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    state = django_filters.CharFilter(method='get_state', field_name='state')
    country = django_filters.CharFilter(method='get_country', field_name='country')  # noqa 502
    district = django_filters.CharFilter(method='get_district', field_name='district')  # noqa 502
    type = django_filters.NumberFilter(method='get_type', field_name='type')
    week = django_filters.NumberFilter(method='get_week', field_name='week')

    o = django_filters.OrderingFilter(
        fields=(
            ('team', 'team'),
            ('year', 'year'),
        ),
    )

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)  # noqa 701
        return queryset

    def get_event(self, queryset, field_name, value):
        if value: return queryset.filter(event=value)  # noqa 701
        return queryset

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)  # noqa 701
        return queryset

    def get_state(self, queryset, field_name, value):
        if value: return queryset.filter(state=value)  # noqa 701
        return queryset

    def get_country(self, queryset, field_name, value):
        if value: return queryset.filter(country=value)  # noqa 701
        return queryset

    def get_district(self, queryset, field_name, value):
        if value: return queryset.filter(district=value)  # noqa 701
        return queryset

    def get_type(self, queryset, field_name, value):
        if value: return queryset.filter(type=value)  # noqa 701
        return queryset

    def get_week(self, queryset, field_name, value):
        if value: return queryset.filter(week=value)  # noqa 701
        return queryset

    class Meta:
        model = TeamEvent
        fields = ['year', 'event', 'team', 'country', 'state', 'district',
                  'type', 'week']


class MatchFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    event = django_filters.CharFilter(method='get_event', field_name='event')
    playoff = django_filters.NumberFilter(method='get_playoff', field_name='playoff')  # noqa 701

    o = django_filters.OrderingFilter(
        fields=(
            ('year', 'year'),
        )
    )

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)  # noqa 701
        return queryset

    def get_event(self, queryset, field_name, value):
        if value: return queryset.filter(event=value)  # noqa 701
        return queryset

    def get_playoff(self, queryset, field_name, value):
        if value: return queryset.filter(playoff=value)  # noqa 701
        return queryset

    class Meta:
        model = Match
        fields = ['year', 'event', 'playoff']


class TeamMatchFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    event = django_filters.CharFilter(method='get_event', field_name='event')
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    playoff = django_filters.NumberFilter(method='get_playoff', field_name='playoff')  # noqa 701

    o = django_filters.OrderingFilter(
        fields=(
            ('team', 'team'),
            ('year', 'year'),
        ),
    )

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)  # noqa 701
        return queryset

    def get_event(self, queryset, field_name, value):
        if value: return queryset.filter(event=value)  # noqa 701
        return queryset

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)  # noqa 701
        return queryset

    def get_playoff(self, queryset, field_name, value):
        if value: return queryset.filter(playoff=value)  # noqa 701
        return queryset

    class Meta:
        model = TeamMatch
        fields = ['year', 'event', 'team', 'playoff']
