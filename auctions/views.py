from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        lots = Lot.objects.all()        
        return render(request, "auctions/index.html",{
            "lots" : lots            
        })

@login_required(login_url='login')
def lot_detail(request, lot_id):
    lot = Lot.objects.get(pk = lot_id)
    comments = Comment.objects.filter(lot = lot)
    comment_form = CommentForm()
    return render(request, 'auctions/lot_detail.html', {
        'lot' : lot,
        'comment_form':comment_form,
        'comments' : comments})

@login_required(login_url='login')
def comment_add(request, lot_id):
    lot = Lot.objects.get(pk = lot_id)
    comment_form = CommentForm()
    if request.method == 'POST':
        bound_form = CommentForm(request.POST)
        if bound_form.is_valid():
            comment = bound_form.save(commit=False)
            comment.comment_user_name = request.user.username
            comment.lot = lot
            comment.save()
            comments = Comment.objects.filter(lot = lot)
            return render(request, 'auctions/lot_detail.html', {
                                                                'lot':lot,
                                                                'comment_form':comment_form,
                                                                'comments':comments})
        else:
            return render(request, "auctions/lot_detail.html", {"lot":lot, "comment_form":bound_form})

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
