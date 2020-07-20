from django.db import models


class Year(models.Model):
    year = models.IntegerField(primary_key=True)  # ex: 2019
    elo_acc = models.FloatField()  # ex: 0.70
    elo_mse = models.FloatField()  # ex: 0.17
    opr_acc = models.FloatField()  # ex: 0.70
    opr_mse = models.FloatField()  # ex: 0.17
    mix_acc = models.FloatField()  # ex: 0.70
    mix_mse = models.FloatField()  # ex: 0.17
    rp1_acc = models.FloatField()  # ex: 0.70
    rp1_mse = models.FloatField()  # ex: 0.17
    rp2_acc = models.FloatField()  # ex: 0.70
    rp2_mse = models.FloatField()  # ex: 0.17
    score_sd = models.FloatField()  # ex: 14.21
    score_mean = models.FloatField()  # ex: 45.12


class Team(models.Model):
    team = models.IntegerField(primary_key=True)  # ex: 5511
    name = models.CharField(max_length=50)  # ex: Cortechs Robotics
    state = models.CharField(max_length=10)  # ex: CA
    country = models.CharField(max_length=30)  # ex: Israel
    district = models.CharField(max_length=10)  # ex: FNC
    active = models.BooleanField()  # ex: True
    elo = models.IntegerField()  # ex: 1700
    elo_recent = models.IntegerField()  # ex: 1600
    elo_mean = models.IntegerField()  # ex: 1600
    elo_max = models.IntegerField()  # ex: 1900


class TeamYear(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField()  # ex: 2019
    team = models.IntegerField()  # ex: 5511
    name = models.CharField(max_length=50)  # ex: Cortechs Robotics
    state = models.CharField(max_length=10)  # ex: California
    country = models.CharField(max_length=30)  # ex: Israel
    district = models.CharField(max_length=10)  # ex: fnc
    elo_start = models.IntegerField()  # ex: 1746
    elo_pre_champs = models.IntegerField()  # ex: 1746
    elo_end = models.IntegerField()  # ex: 1746
    elo_mean = models.IntegerField()  # ex: 1746
    elo_max = models.IntegerField()  # ex: 1746
    elo_diff = models.IntegerField()  # ex: 100
    opr = models.FloatField()  # ex: 12.34
    opr_auto = models.FloatField()  # ex: 12.34
    opr_teleop = models.FloatField()  # ex: 12.34
    opr_1 = models.FloatField()  # ex: 12.34
    opr_2 = models.FloatField()  # ex: 12.34
    opr_endgame = models.FloatField()  # ex: 12.34
    opr_fouls = models.FloatField()  # ex: 12.34
    opr_no_fouls = models.FloatField()  # ex: 12.34
    ils_1 = models.FloatField()  # ex: 50
    ils_2 = models.FloatField()  # ex: 50

    class Meta:
        unique_together = ("year", "team")


class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField()  # ex: 2019
    key = models.CharField(max_length=10)  # ex: ncwak
    name = models.CharField(max_length=100)  # ex: NC Wake County District...
    state = models.CharField(max_length=10)  # ex: NC
    country = models.CharField(max_length=30)  # ex: Israel
    district = models.CharField(max_length=10)  # ex: FNC
    type = models.IntegerField()  # ex: 1
    week = models.IntegerField()  # ex: 2
    time = models.IntegerField()  # ex: 12451261
    elo_top8 = models.IntegerField()  # ex: 1800
    elo_top24 = models.IntegerField()  # ex: 1700
    elo_mean = models.IntegerField()  # ex: 1600
    opr_top8 = models.FloatField()  # ex: 12.34
    opr_top24 = models.FloatField()  # ex: 12.34
    opr_mean = models.FloatField()  # ex: 12.34


class TeamEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    team = models.IntegerField()  # ex: 5511
    year = models.IntegerField()  # ex: 2019
    event = models.CharField(max_length=10)  # ex: ncwak
    state = models.CharField(max_length=10)  # ex: NC
    country = models.CharField(max_length=30)  # ex: Israel
    district = models.CharField(max_length=10)  # ex: FNC
    type = models.IntegerField()  # ex: 1
    week = models.IntegerField()  # ex: 2
    time = models.IntegerField()  # ex: 12451261
    elo_start = models.IntegerField()  # ex: 1746
    elo_pre_playoffs = models.IntegerField()  # ex: 1746
    elo_end = models.IntegerField()  # ex: 1746
    elo_mean = models.IntegerField()  # ex: 1746
    elo_max = models.IntegerField()  # ex: 1746
    elo_diff = models.IntegerField()  # ex: 100
    opr_start = models.FloatField()  # ex: 12.34
    opr_end = models.FloatField()  # ex: 12.34
    opr_auto = models.FloatField()  # ex: 12.34
    opr_teleop = models.FloatField()  # ex: 12.34
    opr_1 = models.FloatField()  # ex: 12.34
    opr_2 = models.FloatField()  # ex: 12.34
    opr_endgame = models.FloatField()  # ex: 12.34
    opr_fouls = models.FloatField()  # ex: 12.34
    opr_no_fouls = models.FloatField()  # ex: 12.34
    ils_1_start = models.FloatField()  # ex: 0.52
    ils_2_start = models.FloatField()  # ex: 0.52
    ils_1_end = models.FloatField()  # ex: 0.52
    ils_2_end = models.FloatField()  # ex: 0.52

    class Meta:
        unique_together = ("year", "event", "team")


class Match(models.Model):
    id = models.IntegerField(primary_key=True)  # ex: 123
    year = models.IntegerField()  # ex: 2020
    event = models.CharField(max_length=10)  # ex: 2020ncwak
    key = models.CharField(max_length=20)  # ex: 2020ncwak_qm1
    comp_level = models.CharField(max_length=10)  # ex: f
    set_number = models.IntegerField()  # ex: 2
    match_number = models.IntegerField()  # ex: 65
    playoff = models.IntegerField()  # ex: 1
    time = models.IntegerField()  # ex: 12451261
    red = models.CharField(max_length=20)  # ex: 5511,254,1678
    blue = models.CharField(max_length=20)  # ex: 5511,254,1678
    red_score = models.IntegerField()  # ex: 50
    blue_score = models.IntegerField()  # ex: 75
    winner = models.CharField(max_length=10)  # ex: blue
    elo_winner = models.CharField(max_length=10)  # ex: blue
    elo_win_prob = models.FloatField()  # ex: 0.60
    opr_winner = models.CharField(max_length=10)  # ex: blue
    opr_win_prob = models.FloatField()  # ex: 0.60
    mix_winner = models.CharField(max_length=10)  # ex: blue
    mix_win_prob = models.FloatField()  # ex: 0.60
    red_rp_1 = models.IntegerField()  # ex: 1
    red_rp_1_prob = models.FloatField()  # ex: 0.60
    red_rp_2 = models.IntegerField()  # ex: 1
    red_rp_2_prob = models.FloatField()  # ex: 0.60
    blue_rp_1 = models.IntegerField()  # ex: 1
    blue_rp_1_prob = models.FloatField()  # ex: 0.60
    blue_rp_2 = models.IntegerField()  # ex: 1
    blue_rp_2_prob = models.FloatField()  # ex: 0.60
    red_auto = models.IntegerField()  # ex: 10
    blue_auto = models.IntegerField()  # ex: 10
    red_teleop = models.IntegerField()  # ex: 10
    blue_teleop = models.IntegerField()  # ex: 10
    red_1 = models.IntegerField()  # ex: 10
    blue_1 = models.IntegerField()  # ex: 10
    red_2 = models.IntegerField()  # ex: 10
    blue_2 = models.IntegerField()  # ex: 10
    red_endgame = models.IntegerField()  # ex: 10
    blue_endgame = models.IntegerField()  # ex: 10
    red_fouls = models.IntegerField()  # ex: 10
    blue_fouls = models.IntegerField()  # ex: 10
    red_no_fouls = models.IntegerField()  # ex: 10
    blue_no_fouls = models.IntegerField()  # ex: 10


class TeamMatch(models.Model):
    id = models.IntegerField(primary_key=True)
    team = models.IntegerField()  # ex: 5511
    year = models.IntegerField()  # ex: 2019
    event = models.CharField(max_length=10)  # ex: ncwak
    match = models.CharField(max_length=10)  # ex: sf1m1
    playoff = models.IntegerField()
    alliance = models.CharField(max_length=10)  # ex: red
    time = models.IntegerField()  # ex: 12451261
    elo = models.IntegerField()  # ex: 1746
    opr = models.FloatField()  # ex: 12.34
    ils_1 = models.FloatField()  # ex: 0.61
    ils_2 = models.FloatField()  # ex: 0.51

    class Meta:
        unique_together = ("year", "event", "match", "team")
