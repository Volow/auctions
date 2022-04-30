from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Max


from .models import *
from .forms import *
from .util import biggest_bid


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        lots = Lot.objects.all()        
        return render(request, "auctions/index.html",{
            "lots" : lots            
        })

def closelist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        lots = Lot.objects.all()        
        return render(request, "auctions/closelist.html",{
            "lots" : lots            
        })



@login_required(login_url='login')
def lot_detail(request, lot_id):
    lot = get_object_or_404(Lot, pk = lot_id)
    watchlist_counter = WatchList.objects.filter(watchlist_user = request.user, watchlist_lot = lot_id).count()
    bids = Bid.objects.filter(bid_lot = lot)

    bid = biggest_bid(bids)
    comments = Comment.objects.filter(lot = lot)
    bid_form = BidForm()
    comment_form = CommentForm() 

    try:
        winner = Bid.objects.filter(bid_lot=lot).latest('bid')
    except:
        winner = None

    # bid_form = BidForm()
    return render(request, 'auctions/lot_detail.html', {
        'lot' : lot,
        'comment_form' : comment_form,
        'bid_form' : bid_form,
        'comments' : comments,
        'bid': bid,
        'watchlist_counter':watchlist_counter,
        'winner': winner})

def lot_close(request, lot_id):
    if request.method == 'POST':
        lot = get_object_or_404(Lot, pk = lot_id)
        lot.lot_status = False
        lot.save()
        try:
            winner_bid = Bid.objects.filter(bid_lot = lot).latest('bid')
            Winner.objects.create(winner_user = winner_bid.bid_user, winner_lot = lot)
        except:
            pass       
        return redirect(lot)

@login_required(login_url='login')
def comment_add(request, lot_id):
    lot = Lot.objects.get(pk = lot_id)    
    if request.method == 'POST':
        bound_form = CommentForm(request.POST)
        if bound_form.is_valid():
            comment = bound_form.save(commit=False)
            comment.comment_user_name = request.user.username
            comment.lot = lot
            comment.save()
            return redirect(lot)
        else:
            return render(request, "auctions/lot_detail.html", {"lot":lot, "comment_form":bound_form})

def bid_add(request, lot_id):
    lot = get_object_or_404(Lot, pk = lot_id)
    comments = Comment.objects.filter(lot = lot)
    comment_form = CommentForm()
    bids = Bid.objects.filter(bid_lot = lot)
    bid = biggest_bid(bids)
    
    if request.method == 'POST':
        bound_form = BidForm(request.POST)
        context = {'lot': lot, 'bid_form': bound_form, 'bid': bid, 'comments' : comments, 'comment_form':comment_form, }
        if bound_form.is_valid():
            if bound_form.cleaned_data['bid'] <= (lot.lot_price and bid):
                bound_form.add_error('bid', 'Bib must be bigger then price and last bid')
                return render(request, 'auctions/lot_detail.html', context)
                # return redirect(lot, ver = "one")
            else:
                bid = bound_form.save(commit=False)
                bid.bid_user = request.user
                bid.bid_lot = lot
                bid.save()
                return redirect(lot)
        else:
            return render(request, "auctions/lot_detail.html", context)


def add_to_watchlist(request, lot_id):
    if request.method == 'POST':
        lot = get_object_or_404(Lot, pk = lot_id, lot_status = True)
        WatchList.objects.create(watchlist_lot = lot, watchlist_user = request.user)
        return redirect('watchlist')

def watchlist_lot_delete(request, lot_id):
    watchlist_record = get_object_or_404(WatchList, pk = lot_id)
    if request.method == 'POST':
        watchlist_record.delete()
        return redirect('watchlist')


@login_required(login_url='login')
def watchlist(request):
    try:
        lots = WatchList.objects.filter(watchlist_user = request.user)
    except:
        lots = None
    # lots = watchlist_lots.watchlist_lot

    return render(request, 'auctions/watchlist.html', {'lots' : lots})


                

@login_required(login_url='login')
def catigory_list(request):
    catigories = Catigory.objects.all()
    if request.method == 'POST':
        bound_form = CatigoryForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()            
            return redirect('catigories_list_url')
        else:
            return render(request, 'auctions/catigories_list.html', {"form": bound_form, "catigories": catigories})
    else:
        form = CatigoryForm()
        return render(request, 'auctions/catigories_list.html', {"form" : form, "catigories": catigories})


@login_required(login_url = 'login')

def lot_add(request):
    catigories = Catigory.objects.all()
    if request.method == 'POST':
        bound_form = LotForm(request.POST, request.FILES)
        if bound_form.is_valid():
            lot = bound_form.save(commit=False)           
            lot.lot_owner = request.user
            lot.save()
            return redirect('index')
        else:
            return render(request, 'auctions/lot_add.html', {"form":bound_form, "catigories" : catigories})
    return render(request, "auctions/lot_add.html",{
        "form": LotForm(),
        "catigories" : catigories
    })



@login_required(login_url = 'login')
def catigory_delete(request, catigory_id):
    catigory = Catigory.objects.get(pk = catigory_id)
    if request.method == 'POST':
        catigory.delete()
    return redirect('catigories_list_url')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
