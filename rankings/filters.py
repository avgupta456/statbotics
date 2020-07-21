import django_filters

from .models import Event, Match, Team, TeamEvent, TeamMatch, TeamYear, Year


def get_year(queryset, field_name, value):
    if value:
        return queryset.filter(year=value)
    return queryset


def get_team(queryset, field_name, value):
    if value:
        return queryset.filter(team=value)
    return queryset


def get_active(queryset, field_name, value):
    if value:
        return queryset.filter(active=value)
    return queryset


def get_state(queryset, field_name, value):
    if value:
        return queryset.filter(state=value)
    return queryset


def get_country(queryset, field_name, value):
    if value:
        return queryset.filter(country=value)
    return queryset


def get_district(queryset, field_name, value):
    if value:
        return queryset.filter(district=value)
    return queryset


def get_key(queryset, field_name, value):
    if value:
        return queryset.filter(key=value)
    return queryset


def get_type(queryset, field_name, value):
    if value:
        return queryset.filter(type=value)
    return queryset


def get_week(queryset, field_name, value):
    if value:
        return queryset.filter(week=value)
    return queryset


def get_event(queryset, field_name, value):
    if value:
        return queryset.filter(event=value)
    return queryset


def get_playoff(queryset, field_name, value):
    if value:
        return queryset.filter(playoff=value)
    return queryset


class YearFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method=get_year, field_name="year")

    o = django_filters.OrderingFilter(
        fields=(
            ("elo_acc", "elo_acc"),
            ("elo_mse", "elo_mse"),
            ("opr_acc", "opr_acc"),
            ("opr_mse", "opr_mse"),
            ("mix_acc", "mix_acc"),
            ("mix_mse", "mix_mse"),
        ),
    )

    class Meta:
        model = Year
        fields = ["year"]


class TeamFilterSet(django_filters.FilterSet):
    team = django_filters.NumberFilter(method=get_team, field_name="team")
    active = django_filters.NumberFilter(method=get_active, field_name="active")
    state = django_filters.CharFilter(method=get_state, field_name="state")
    country = django_filters.CharFilter(method=get_country, field_name="country")
    district = django_filters.CharFilter(method=get_district, field_name="district")

    o = django_filters.OrderingFilter(
        fields=(
            ("team", "team"),
            ("elo", "elo"),
            ("elo_recent", "elo_recent"),
            ("elo_mean", "elo_mean"),
            ("elo_max", "elo_max"),
        ),
    )

    class Meta:
        model = Team
        fields = ["team", "active", "state", "country", "district"]


class TeamYearFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method=get_year, field_name="year")
    team = django_filters.NumberFilter(method=get_team, field_name="team")
    state = django_filters.CharFilter(method=get_state, field_name="state")
    country = django_filters.CharFilter(method=get_country, field_name="country")
    district = django_filters.CharFilter(method=get_district, field_name="district")

    o = django_filters.OrderingFilter(
        fields=(
            ("year", "year"),
            ("team", "team"),
            ("elo_start", "elo_start"),
            ("elo_pre_champs", "elo_pre_champs"),
            ("elo_end", "elo_end"),
            ("elo_mean", "elo_mean"),
            ("elo_max", "elo_max"),
        ),
    )

    class Meta:
        model = TeamYear
        fields = ["year", "team", "state", "country", "district"]


class EventFilterSet(django_filters.FilterSet):
    key = django_filters.CharFilter(method=get_key, field_name="key")
    year = django_filters.NumberFilter(method=get_year, field_name="year")
    state = django_filters.CharFilter(method=get_state, field_name="state")
    country = django_filters.CharFilter(method=get_country, field_name="country")
    district = django_filters.CharFilter(method=get_district, field_name="district")
    type = django_filters.NumberFilter(method=get_type, field_name="type")
    week = django_filters.NumberFilter(method=get_week, field_name="week")

    o = django_filters.OrderingFilter(
        fields=(
            ("year", "year"),
            ("elo_top8", "elo_top8"),
            ("elo_top24", "elo_top24"),
            ("elo_mean", "elo_mean"),
        ),
    )

    class Meta:
        model = Event
        fields = ["key", "year", "country", "state", "district", "type", "week"]


class TeamEventFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method=get_year, field_name="year")
    event = django_filters.CharFilter(method=get_event, field_name="event")
    team = django_filters.NumberFilter(method=get_team, field_name="team")
    state = django_filters.CharFilter(method=get_state, field_name="state")
    country = django_filters.CharFilter(method=get_country, field_name="country")
    district = django_filters.CharFilter(method=get_district, field_name="district")
    type = django_filters.NumberFilter(method=get_type, field_name="type")
    week = django_filters.NumberFilter(method=get_week, field_name="week")

    o = django_filters.OrderingFilter(fields=(("team", "team"), ("year", "year"),),)

    class Meta:
        model = TeamEvent
        fields = [
            "year",
            "event",
            "team",
            "country",
            "state",
            "district",
            "type",
            "week",
        ]


class MatchFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method=get_year, field_name="year")
    event = django_filters.CharFilter(method=get_event, field_name="event")
    playoff = django_filters.NumberFilter(method=get_playoff, field_name="playoff")

    o = django_filters.OrderingFilter(fields=(("year", "year"),))

    class Meta:
        model = Match
        fields = ["year", "event", "playoff"]


class TeamMatchFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(method=get_year, field_name="year")
    event = django_filters.CharFilter(method=get_event, field_name="event")
    team = django_filters.NumberFilter(method=get_team, field_name="team")
    playoff = django_filters.NumberFilter(method=get_playoff, field_name="playoff")

    o = django_filters.OrderingFilter(fields=(("team", "team"), ("year", "year"),),)

    class Meta:
        model = TeamMatch
        fields = ["year", "event", "team", "playoff"]
