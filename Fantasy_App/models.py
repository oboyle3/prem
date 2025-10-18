from django.db import models
class Team(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    stadium = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
