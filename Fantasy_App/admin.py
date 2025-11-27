from django.contrib import admin
from .models import Team, UserProfile , Game, Match


admin.site.register(Team)
admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Match)
