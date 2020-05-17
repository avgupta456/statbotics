from django.db import models

class Team(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.number) + "(" + self.name + ")"
