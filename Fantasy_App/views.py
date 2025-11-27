from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .scraper import get_premier_league_table
from .models import Team, UserProfile
from .forms import PredictionForm
from .models import Game, Prediction , Team
from django.shortcuts import render, get_object_or_404, redirect
def landing(request):
    return render(request, 'landing.html')

# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')
#path('dashboard/',views.dashboard,name='dashboard'),
#path('change_fav_team/',viewschange_fav_team,name='change_fav_team'),
@login_required
def dashboard(request):
     # Access the user's favorite team
     #print("team list view hit")
     teams = Team.objects.all()
     profile = UserProfile.objects.get(user=request.user) #will return oboyle3 (user)
     print(profile)
     favorite_team = profile.favorite_team #willl return users favorite team
     print(favorite_team)
     #teams = Team.objects.all()
     table = get_premier_league_table()
     headers = table[0]
     rows = table[1:]
     return render(request, "dashboard.html", {
        "headers": headers,
        "rows": rows,
        'favorite_team': favorite_team,
        "teams": teams,
        
    })
   # return render(request,'dashboard.html',{'teams':teams})


@login_required
def game_list(request):
    games = Game.objects.all().order_by('date')
    return render(request, 'dashboard.html', {'games': games})


@login_required
def change_fav_team(request):
    print("made it to Change fav team !!")
    profile = request.user.userprofile  
    print("here is the profile")
    print (profile)
    print("-----")
    teams = Team.objects.all()
    print(teams)

    if request.method == "POST":
        print ("we identify a post function here is the id: ")
        profile.favorite_team_id = request.POST.get("favorite_team")
        print("Selected team ID:", profile.favorite_team_id)
        profile.save()
        return redirect("dashboard")

    return render(request, "change_fav_team.html", {
        "profile": profile,
        "teams": teams,
    })

