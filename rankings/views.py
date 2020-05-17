from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import TeamSerializer
from .serializers import UserSerializer

from .models import Team
from django.contrib.auth.models import User

class TeamView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
