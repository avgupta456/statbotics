"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rankings import views

router = routers.DefaultRouter()
router.register(r'team_matches', views.TeamMatchView, 'team_match')
router.register(r'team_events', views.TeamEventView, 'team_event')
router.register(r'team_years', views.TeamYearView, 'team_year')
router.register(r'teams', views.TeamView, 'team')
router.register(r'events', views.EventView, 'event')
router.register(r'years', views.YearView, 'year')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
