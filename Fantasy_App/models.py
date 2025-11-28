from django.db import models
from django.contrib.auth.models import User
class Team(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    stadium = models.CharField(max_length=100, blank=True, null=True)
    #played_games = models.IntegerField()

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    opponent = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    tv_channel = models.CharField(max_length=50, blank=True)
    home_game = models.BooleanField(default=True)
    result = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('W', 'Win'),
        ('L', 'Loss'),
        ('TBD', 'TBD')
    ])

    def __str__(self):
        return f"{'vs' if self.home_game else '@'} {self.opponent} on {self.date}"

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=10, choices=[
        ('Win', 'Win'),
        ('Loss', 'Loss'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')  # Prevent duplicate predictions

    def __str__(self):
        return f"{self.user.username}: {self.game.opponent} → {self.prediction}"


class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name="home_matches", on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_matches", on_delete=models.CASCADE)
    match_date = models.DateTimeField()
    venue = models.CharField(max_length=100, blank=True, null=True)
    result = models.CharField(max_length=20, blank=True, null=True)  # optional: score like "2-1"

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.match_date.strftime('%Y-%m-%d')}"
    


class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    total_supply = models.PositiveBigIntegerField(default=10_000_000)

    def __str__(self):
        return self.name
    
class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"self.user.username Wallet"
    


class Stock(models.model):
    symbol = models.Charfield(max_length=10, unique = True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=10, unique=True)
    total_supply = models.PositiveIntegerField(default=0) #how many shares exist
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"