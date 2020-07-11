from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Year, Team, TeamYear, Event, TeamEvent, Match, TeamMatch


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamYear
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TeamEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamEvent
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class TeamMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatch
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
