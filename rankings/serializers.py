from rest_framework import serializers

from .models import Team
from django.contrib.auth.models import User

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('number', 'name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
