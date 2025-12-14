from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
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
    


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique = True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=10, unique=True)
    total_supply = models.PositiveIntegerField(default=0) #how many shares exist
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"
    

'''class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username '''



class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "stock")



class GolfersInDatabase(models.Model):
    name = models.CharField(max_length=50)
    hometown = models.CharField(max_length=100, default="Monroe NY:)")
    tour = models.CharField(max_length=100, default="PGA")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    def __str__(self):
        return self.name
    

def validate_max_five(value):
    if value.count() > 5:
        raise ValidationError("You can only track up to 5 golfers.")


class UserTrackedGolfers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 5 selection slots
    selection1 = models.ForeignKey(
        GolfersInDatabase,
        null=True, blank=True,
        related_name="slot1_users",
        on_delete=models.SET_NULL,
    )
    selection2 = models.ForeignKey(
        GolfersInDatabase,
        null=True, blank=True,
        related_name="slot2_users",
        on_delete=models.SET_NULL,
    )
    selection3 = models.ForeignKey(
        GolfersInDatabase,
        null=True, blank=True,
        related_name="slot3_users",
        on_delete=models.SET_NULL,
    )
    selection4 = models.ForeignKey(
        GolfersInDatabase,
        null=True, blank=True,
        related_name="slot4_users",
        on_delete=models.SET_NULL,
    )
    selection5 = models.ForeignKey(
        GolfersInDatabase,
        null=True, blank=True,
        related_name="slot5_users",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.user.username}'s lineup"




class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    

class GolferScore(models.Model):
    golfer = models.ForeignKey(GolfersInDatabase, on_delete=models.CASCADE, related_name="scores")
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="scores")

    round_number = models.IntegerField()  # 1,2,3,4 = Thu/Fri/Sat/Sun
    score = models.IntegerField()  # e.g., 70
    relative_to_par = models.IntegerField(null=True, blank=True)  # -3, +2, etc.

    def __str__(self):
        return f"{self.golfer.name} - R{self.round_number} - {self.score}"
    


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=10, unique=True)

    def __str__(self):
            return self.title
    


class AllGolfers(models.Model):
    name = models.CharField(max_length=100)
    hometown = models.CharField(max_length=100, blank=True)
    tour = models.CharField(max_length=50)
    rating = models.IntegerField()

    day_1_score_Masters26 = models.IntegerField(null=True, blank=True)
    day_2_score_Masters26 = models.IntegerField(null=True, blank=True)
    day_3_score_Masters26 = models.IntegerField(null=True, blank=True)
    day_4_score_Masters26 = models.IntegerField(null=True, blank=True)

    def total_score(self):
        return (
            (self.day_1_score_Masters26 or 0) +
            (self.day_2_score_Masters26 or 0) +
            (self.day_3_score_Masters26 or 0) +
            (self.day_4_score_Masters26 or 0)
        )

    def __str__(self):
        return self.name
