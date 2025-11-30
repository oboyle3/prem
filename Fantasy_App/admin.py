from django.contrib import admin
from .models import Team, UserProfile 
from .models import  Game, Match
from .models import Wallet, Currency, GolfersInDatabase, UserTrackedGolfers



admin.site.register(Team)
admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Match)
admin.site.register(Wallet)
admin.site.register(Currency)
admin.site.register(GolfersInDatabase)
admin.site.register(UserTrackedGolfers)
