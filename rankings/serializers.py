from rest_framework import serializers

from .models import TeamMatch, TeamEvent, TeamYear, Team, Event, Year
from django.contrib.auth.models import User

class TeamMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatch
        fields = ('id', 'year', 'event', 'match',
            'team', 'elo_start', 'elo_end', 'elo_diff')

class TeamEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamEvent
        fields = ('id', 'year', 'event', 'team', 'elo_start',
            'elo_pre_playoffs', 'elo_end', 'elo_mean', 'elo_max', 'elo_diff')

class TeamYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamYear
        fields = ('id', 'year', 'team', 'elo_start', 'elo_pre_champs',
            'elo_end', 'elo_mean', 'elo_max', 'elo_diff', 'rank', 'percentile')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('team', 'elos',  'elo_mean', 'elo_max', 'elo_max_year')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'year', 'event', 'elo_max', 'elo_top8', 'elo_top24', 'elo_mean', 'elo_sd')

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ('year', 'elo_max', 'elo_1p', 'elo_5p', 'elo_10p', 'elo_25p',
            'elo_median', 'elo_mean', 'elo_sd', 'acc', 'mse')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
