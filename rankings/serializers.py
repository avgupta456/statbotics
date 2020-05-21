from rest_framework import serializers

from .models import TeamMatch, TeamEvent, TeamYear, Team, Event, Year
from django.contrib.auth.models import User

class TeamMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatch
        fields = ['year', 'event', 'match', 'team', 'elo_start', 'elo_end', 'elo_diff']

class TeamEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamEvent
        fields = '__all__'

class TeamYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamYear
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
