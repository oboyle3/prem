from pyexpat.errors import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .scraper import get_premier_league_table
from .models import Team, UserProfile, UserStock ,Wallet, Currency
from .forms import BuyStockForm, PredictionForm , StockForm
from .models import Game, Prediction , Team, Stock , GolfersInDatabase
from django.contrib.auth.forms import UserCreationForm
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
     golfers = GolfersInDatabase.objects.all()
     stocks = Stock.objects.all()
     print("these are the stocks:", stocks)
     print("GOLFERS:", golfers)
     wallet = request.user.wallet
     currency = Currency.objects.first()
     teams = Team.objects.all()
     profile = UserProfile.objects.get(user=request.user) #will return oboyle3 (user)
     #print(profile)
     favorite_team = profile.favorite_team #willl return users favorite team
     #print(favorite_team)
     #teams = Team.objects.all()
     table = get_premier_league_table()
     headers = table[0]
     rows = table[1:]
     return render(request, "dashboard.html", {
        "headers": headers,
        "rows": rows,
        'favorite_team': favorite_team,
        "teams": teams,
        "wallet": wallet,
        "currency": currency,
        "stocks": stocks,
        "golfers": golfers,
        
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



@login_required
def withdraw(request):
    print("withdraw function called")

    user = request.user
    print("user requesting:", user)

    wallet = user.wallet  
    print(user, "has this much in their wallet:", wallet.balance)

    currency = Currency.objects.first()
    print(currency, "This is the amount in the economy:", currency.total_supply)

    if request.method == "POST":
        print("1) user hit post")
        amount = int(request.POST.get("amount"))
        print("2) for amount ", amount)
        # Process withdrawal
        wallet.balance += amount
        wallet.save()
        currency.total_supply -= amount
        currency.save()
        return redirect("dashboard")


    return render(request, "withdraw.html", {"wallet": wallet})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()  # <-- IMPORTANT

    return render(request, "signup.html", {"form": form})





def addstock(request):
    print("=== Add Stock View Hit ===")

    if request.method == "POST":
        print("Request method: POST")
        print("POST DATA:", request.POST)

        form = StockForm(request.POST)
        print("Form created:", form)

        if form.is_valid():
            print("Form is VALID ✔")
            stock = form.save()
            print("Saved stock:", stock)
            return redirect("dashboard")
        else:
            print("Form is NOT valid ")
            print("FORM ERRORS:", form.errors)

    else:
        print("Request method: GET (displaying form)")
        form = StockForm()

    return render(request, "addstock.html", {"form": form})



def premtable(request):
    return render(request, 'premtable.html')


@login_required
def buy_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    wallet = request.user.wallet

    if request.method == "POST":
        qty = int(request.POST.get("quantity", 0))
        cost = qty * stock.price

        if qty <= 0:
            return render(request, "buy_stock.html", {
                "stock": stock,
                "error": "Invalid quantity."
            })

        if wallet.balance < cost:
            return render(request, "buy_stock.html", {
                "stock": stock,
                "error": "Not enough balance."
            })

        if stock.total_supply < qty:
            return render(request, "buy_stock.html", {
                "stock": stock,
                "error": "Not enough supply available."
            })

        # Perform purchase
        wallet.balance -= cost
        wallet.save()

        stock.total_supply -= qty
        stock.save()

        UserStock.objects.create(
            user=request.user,
            stock=stock,
            shares=qty
        )

        return render(request, "buy_stock.html", {
            "stock": stock,
            "success": "Purchase successful!"
        })

    return render(request, "buy_stock.html", {"stock": stock})
