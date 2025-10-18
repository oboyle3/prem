from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .scraper import get_premier_league_table
from .models import Team
def landing(request):
    return render(request, 'landing.html')

# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')

@login_required
def dashboard(request):
    #teams = Team.objects.all()
    table = get_premier_league_table()
    headers = table[0]
    rows = table[1:]
    return render(request, "dashboard.html", {
        "headers": headers,
        "rows": rows
    })
   # return render(request,'dashboard.html',{'teams':teams})