from django.db import models
from django.core.validators import validate_comma_separated_integer_list

class TeamMatch(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField() #ex: 2019
    event = models.CharField(max_length=10) #ex: ncwak
    match = models.CharField(max_length=10) #ex: sf1m1
    team = models.IntegerField() #ex: 5511
    start_elo = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    end_elo = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_diff = models.DecimalField(max_digits=6, decimal_places=2) #ex: 100

    class Meta:
        unique_together = (("year", "event", "match", "team"))

class TeamEvent(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField() #ex: 2019
    event = models.CharField(max_length=10) #ex: ncwak
    team = models.IntegerField() #ex: 5511
    elo_start = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_pre_playoffs = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_end = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_mean = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_max = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_diff = models.DecimalField(max_digits=6, decimal_places=2) #ex: 100

    class Meta:
        unique_together = (("year", "event", "team"))

class TeamYear(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField() #ex: 2019
    team = models.IntegerField() #ex: 5511
    elo_start = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_pre_champs = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_end = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_mean = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_max = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1746.45
    elo_diff = models.DecimalField(max_digits=6, decimal_places=2) #ex: 100
    rank = models.IntegerField() #ex: 546
    percentile = models.DecimalField(max_digits=6, decimal_places=2) #ex: 5.24

    class Meta:
        unique_together = (("year", "team"))

class Team(models.Model):
    team = models.IntegerField(primary_key=True) #ex: 5511
    elos = models.CharField(max_length=200, validators=[validate_comma_separated_integer_list]) #ex: [1500, 1600, 1400, ...]
    elo_mean = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1600
    elo_max = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1900
    elo_max_year = models.IntegerField() #ex: 2015

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField() #ex: 2019
    event = models.CharField(max_length=10) #ex: ncwak
    elo_max = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1900
    elo_top8 = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1800
    elo_top24 = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1700
    elo_mean = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1600
    elo_sd = models.DecimalField(max_digits=6, decimal_places=2) #ex: 500

class Year(models.Model):
    year = models.IntegerField(primary_key=True) #ex: 2019
    elo_max = models.DecimalField(max_digits=6, decimal_places=2) #ex: 2000
    elo_1p = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1950
    elo_5p = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1900
    elo_10p = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1850
    elo_25p = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1800
    elo_median = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1550
    elo_mean = models.DecimalField(max_digits=6, decimal_places=2) #ex: 1500
    elo_sd = models.DecimalField(max_digits=6, decimal_places=2) #ex: 500
    acc = models.DecimalField(max_digits=6, decimal_places=2) #ex: 0.70
    mse = models.DecimalField(max_digits=6, decimal_places=2) #ex: 0.17
