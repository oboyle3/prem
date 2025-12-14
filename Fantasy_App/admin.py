from django.contrib import admin
from .models import Team, UserProfile 
from .models import  Game, Match
from .models import Wallet, Currency, GolfersInDatabase, UserTrackedGolfers
from .models import Tournament, GolferScore, Book, GolferDBIAMTESTING



admin.site.register(Team)
admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Match)
admin.site.register(Wallet)
admin.site.register(Currency)
admin.site.register(GolfersInDatabase)
admin.site.register(UserTrackedGolfers)
admin.site.register(Tournament)
admin.site.register(GolferScore)
admin.site.register(Book)
admin.site.register(GolferDBIAMTESTING)
