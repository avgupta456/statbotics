from django.db import models

class TeamMatch(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField() #ex: 2019
    event = models.CharField(max_length=10) #ex: ncwak
    match = models.CharField(max_length=10) #ex: sf1m1
    team = models.IntegerField() #ex: 5511
    elo_start = models.IntegerField() #ex: 1746
    elo_end = models.IntegerField() #ex: 1746
    elo_diff = models.IntegerField() #ex: 100

    class Meta:
        unique_together = (("year", "event", "match", "team"))

class TeamEvent(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField() #ex: 2019
    event = models.CharField(max_length=10) #ex: ncwak
    team = models.IntegerField() #ex: 5511
    elo_start = models.IntegerField() #ex: 1746
    elo_pre_playoffs = models.IntegerField() #ex: 1746
    elo_end = models.IntegerField() #ex: 1746
    elo_mean = models.IntegerField() #ex: 1746
    elo_max = models.IntegerField() #ex: 1746
    elo_diff = models.IntegerField() #ex: 100

    class Meta:
        unique_together = (("year", "event", "team"))

class TeamYear(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField() #ex: 2019
    team = models.IntegerField() #ex: 5511
    elo_start = models.IntegerField() #ex: 1746
    elo_pre_champs = models.IntegerField() #ex: 1746
    elo_end = models.IntegerField() #ex: 1746
    elo_mean = models.IntegerField() #ex: 1746
    elo_max = models.IntegerField() #ex: 1746
    elo_diff = models.IntegerField() #ex: 100
    rank = models.IntegerField() #ex: 546
    percentile = models.DecimalField(max_digits=6, decimal_places=4) #ex: 5.24

    class Meta:
        unique_together = (("year", "team"))

class Team(models.Model):
    team = models.IntegerField(primary_key=True) #ex: 5511
    name = models.CharField(max_length=100) #ex: Cortechs Robotics
    region = models.CharField(max_length=30) #ex: California
    district = models.CharField(max_length=10) #ex: FNC
    years_active = models.IntegerField() #ex: 19
    active = models.BooleanField() #ex: True
    elo = models.IntegerField() #ex: 1700
    elo_mean = models.IntegerField() #ex: 1600
    elo_max = models.IntegerField() #ex: 1900
    elo_max_year = models.IntegerField() #ex: 2015

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField() #ex: 2019
    event = models.CharField(max_length=10) #ex: ncwak
    elo_max = models.IntegerField() #ex: 1900
    elo_top8 = models.IntegerField() #ex: 1800
    elo_top24 = models.IntegerField() #ex: 1700
    elo_mean = models.IntegerField() #ex: 1600
    elo_sd = models.IntegerField() #ex: 500

class Year(models.Model):
    year = models.IntegerField(primary_key=True) #ex: 2019
    elo_max = models.IntegerField() #ex: 2000
    elo_1p = models.IntegerField() #ex: 1950
    elo_5p = models.IntegerField() #ex: 1900
    elo_10p = models.IntegerField() #ex: 1850
    elo_25p = models.IntegerField() #ex: 1800
    elo_median = models.IntegerField() #ex: 1550
    elo_mean = models.IntegerField() #ex: 1500
    elo_sd = models.IntegerField() #ex: 500
    acc = models.DecimalField(max_digits=6, decimal_places=4) #ex: 0.70
    mse = models.DecimalField(max_digits=6, decimal_places=4) #ex: 0.17
