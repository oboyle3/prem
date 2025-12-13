from pyexpat.errors import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .scraper import get_premier_league_table
from .models import GolferScore, Team, UserProfile, UserStock ,Wallet, Currency
from .forms import BookForm, BuyStockForm, PredictionForm , StockForm
from .models import Game, Prediction , Team, Stock , GolfersInDatabase
from .models import GolfersInDatabase, UserTrackedGolfers
from zoneinfo import ZoneInfo
from datetime import datetime
from .models import Book
from .forms import BookForm

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
    # -------------------- Your existing queries --------------------
    golfers = GolfersInDatabase.objects.all()
    for g in golfers:
        print(f"ID {g.id} -> {g.name}")
    lineup = UserTrackedGolfers.objects.get(user=request.user)
    stocks = Stock.objects.all()
    wallet = request.user.wallet
    currency = Currency.objects.first()
    teams = Team.objects.all()
    allgolferdata = GolferScore.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    favorite_team = profile.favorite_team

    table = get_premier_league_table()
    headers = table[0]
    rows = table[1:]

    # -------------------- Countdown logic --------------------
    est = ZoneInfo("America/New_York")
    target_date = datetime(2026, 4, 9, 9, 0, 0, tzinfo=est)
    now = datetime.now(est)
    diff = target_date - now

    if diff.total_seconds() > 0:
        days = diff.days
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
    else:
        days = hours = minutes = secs = 0  # Event has passed

    countdown = {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": secs
    }

    # -------------------- Render --------------------
    return render(request, "dashboard.html", {
        "headers": headers,
        "rows": rows,
        "favorite_team": favorite_team,
        "teams": teams,
        "wallet": wallet,
        "currency": currency,
        "stocks": stocks,
        "golfers": golfers,
        "lineup": lineup,
        "allgolferdata": allgolferdata,
        "countdown": countdown,  # Pass countdown to template
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



def select_golfers(request):
    tracking_obj, created = UserTrackedGolfers.objects.get_or_create(user=request.user)
    if request.method == "POST":
        selected_ids = request.POST.getlist("golfers")

        if len(selected_ids) > 5:
            return render(request, "select_golfers.html", {
                "golfers": GolfersInDatabase.objects.all(),
                "error": "You can select a maximum of 5 golfers."
            })

        tracking_obj = UserTrackedGolfers.objects.get(user=request.user)
        tracking_obj.golfers.set(selected_ids)
        return redirect("dashboard")

    return render(request, "select_golfers.html", {
        "golfers": GolfersInDatabase.objects.all()
    })



@login_required
def updateslot2(request):
    golfers = GolfersInDatabase.objects.filter(rating__gte=7, rating__lte=8)
    print("updateslot2:", golfers)
    if request.method == "POST":
        golfer_id = request.POST.get("golfer")

        if golfer_id:
            lineup = UserTrackedGolfers.objects.get(user=request.user)
            lineup.selection2_id = golfer_id
            lineup.save()

        # Redirect to dashboard after saving
        return redirect("dashboard")   # <--- IMPORTANT

    return render(request, 'update_slot2.html', {
        'golfers': golfers
    })

@login_required
def updateslot1(request):
    golfers = GolfersInDatabase.objects.filter(rating__gte=9, rating__lte=10)
    print("updateslot1:", golfers)
    if request.method == "POST":
        golfer_id = request.POST.get("golfer")

        if golfer_id:
            lineup = UserTrackedGolfers.objects.get(user=request.user)
            lineup.selection1_id = golfer_id
            lineup.save()

        # Redirect to dashboard after saving
        return redirect("dashboard")   # <--- IMPORTANT

    return render(request, 'update_slot1.html', {
        'golfers': golfers
    })

@login_required
def updateslot3(request):
    golfers = GolfersInDatabase.objects.filter(rating__gte=5, rating__lte=6)
    print("updateslot3:", golfers)
    if request.method == "POST":
        golfer_id = request.POST.get("golfer")

        if golfer_id:
            lineup = UserTrackedGolfers.objects.get(user=request.user)
            lineup.selection3_id = golfer_id
            lineup.save()

        # Redirect to dashboard after saving
        return redirect("dashboard")   # <--- IMPORTANT

    return render(request, 'update_slot3.html', {
        'golfers': golfers
    })


@login_required
def updateslot4(request):
    golfers = GolfersInDatabase.objects.filter(rating__gte=3, rating__lte=4)
    print("updateslot4:", golfers)
    if request.method == "POST":
        golfer_id = request.POST.get("golfer")

        if golfer_id:
            lineup = UserTrackedGolfers.objects.get(user=request.user)
            lineup.selection4_id = golfer_id
            lineup.save()

        # Redirect to dashboard after saving
        return redirect("dashboard")   # <--- IMPORTANT

    return render(request, 'update_slot4.html', {
        'golfers': golfers
    })


@login_required
def updateslot5(request):
    golfers = GolfersInDatabase.objects.filter(rating__gte=1, rating__lte=2)
    print("updateslot5:", golfers)
    if request.method == "POST":
        golfer_id = request.POST.get("golfer")

        if golfer_id:
            lineup = UserTrackedGolfers.objects.get(user=request.user)
            lineup.selection5_id = golfer_id
            print("lineup selection 2: ", lineup.selection5_id )
            lineup.save()

        # Redirect to dashboard after saving
        return redirect("dashboard")   # <--- IMPORTANT

    return render(request, 'update_slot5.html', {
        'golfers': golfers
    })

@login_required
def allscores(request):
    # Get the logged-in user's selected golfers
    try:
        tracked = UserTrackedGolfers.objects.get(user=request.user)
    except UserTrackedGolfers.DoesNotExist:
        tracked = None

    if tracked:
        selected_golfers = [
            tracked.selection1,
            
            tracked.selection2,
            tracked.selection3,
            tracked.selection4,
            tracked.selection5,
        ]

        scores = GolferScore.objects.filter(golfer__in=selected_golfers)

    else:
        scores = GolferScore.objects.none()

    return render(request, "allscores.html", {"scores": scores})



def mockadmin(request):
    books = Book.objects.all()
    return render(request, 'mockadmin.html',{
        'books': books,
        })
                  



def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('mockadmin')  # back to admin list
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})