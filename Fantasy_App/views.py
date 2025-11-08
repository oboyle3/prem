from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .scraper import get_premier_league_table
from .models import Team, UserProfile
from .forms import PredictionForm
from .models import Game, Prediction
from django.shortcuts import render, get_object_or_404, redirect
def landing(request):
    return render(request, 'landing.html')

# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')

@login_required
def dashboard(request):
     # Access the user's favorite team
    favorite_team = UserProfile.favorite_team
    #teams = Team.objects.all()
    table = get_premier_league_table()
    headers = table[0]
    rows = table[1:]
    return render(request, "dashboard.html", {
        "headers": headers,
        "rows": rows,
        'favorite_team': favorite_team
    })
   # return render(request,'dashboard.html',{'teams':teams})


@login_required
def game_list(request):
    games = Game.objects.all().order_by('date')
    return render(request, 'dashboard.html', {'games': games})
