from .models import (
    TeamMatch,
    TeamEvent,
    TeamYear,
    Team,
    Event,
    Year,
)

import django_filters

class TeamMatchFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    event = django_filters.CharFilter(method='get_event', field_name='event')
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    o = django_filters.OrderingFilter(
        fields=(
            ('time', 'time'),
            ('team', 'team'),
            ('year', 'year'),
        ),
    )

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)
        return queryset

    def get_event(self, queryset, field_name, value):
        if value: return queryset.filter(event=value)
        return queryset

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)
        return queryset

    class Meta:
        model = TeamMatch
        fields = ['year', 'event', 'team']

class TeamEventFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    event = django_filters.CharFilter(method='get_event', field_name='event')
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    o = django_filters.OrderingFilter(
        fields=(
            ('time', 'time'),
            ('team', 'team'),
            ('year', 'year'),
        ),
    )

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)
        return queryset

    def get_event(self, queryset, field_name, value):
        if value: return queryset.filter(event=value)
        return queryset

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)
        return queryset

    class Meta:
        model = TeamEvent
        fields = ['year', 'event', 'team']

class TeamYearFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    o = django_filters.OrderingFilter(
        fields=(
            ('year', 'year'),
            ('team', 'team'),
        ),
    )
    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)
        return queryset

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)
        return queryset

    class Meta:
        model = TeamYear
        fields = ['year', 'team']

class TeamFilterSet(django_filters.FilterSet):
    team = django_filters.NumberFilter(method='get_team', field_name='team')
    active = django_filters.NumberFilter(method='get_active', field_name='active')
    years_active = django_filters.NumberFilter(method='get_years_active', field_name='years_active')
    region = django_filters.CharFilter(method='get_region', field_name='region')
    district = django_filters.CharFilter(method='get_district', field_name='district')
    o = django_filters.OrderingFilter(
        fields=(
            ('team', 'team'),
            ('years_active'),
            ('years_active'),
        ),
    )

    def get_team(self, queryset, field_name, value):
        if value: return queryset.filter(team=value)
        return queryset

    def get_active(self, queryset, field_name, value):
        if value: return queryset.filter(active=value)
        return queryset

    def get_years_active(self, queryset, field_name, value):
        if value: return queryset.filter(years_active=value)
        return queryset

    def get_region(self, queryset, field_name, value):
        if value: return queryset.filter(region=value)
        return queryset

    def get_district(self, queryset, field_name, value):
        if value: return queryset.filter(district=value)
        return queryset

    class Meta:
        model = Team
        fields = ['team', 'active', 'years_active', 'region', 'district']

class EventFilterSet(django_filters.FilterSet):
    event = django_filters.CharFilter(method='get_event', field_name='event')
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    o = django_filters.OrderingFilter(
        fields=(
            ('year', 'year'),
            ('elo_mean', 'elo_mean'),
        ),
    )

    def get_event(self, queryset, field_name, value):
        if value: return queryset.filter(event=value)
        return queryset

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)
        return queryset

    class Meta:
        model = Event
        fields = ['event', 'year']

class YearFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='get_year', field_name='year')
    o = django_filters.OrderingFilter(
        fields=(
            ('elo_max', 'elo_max'),
            ('acc', 'acc'),
            ('mse', 'mse'),
        ),
    )

    def get_year(self, queryset, field_name, value):
        if value: return queryset.filter(year=value)
        return queryset

    class Meta:
        model = Year
        fields = ['year']
