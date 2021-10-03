from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import Error
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, auction_listing
from .forms import listing_form,bid_form,comment_form
# from django.contrib import messages



# def index(request):
#     if request.method=="POST":
#         form=create_form(request.POST)
#         if form.is_valid():
#             print("test1")
#             title=form.cleaned_data["title"]
#             description=form.cleaned_data["description"]
#             url=form.cleaned_data["url"]
#             tag=form.cleaned_data["tag"]
#             amount=form.cleaned_data["amount"]
#             try:
#                 print("test2")
#                 print(datetime.now())
#                 u=User.objects.get(pk=request.user.id)
                
#                 print("test9")
#                 listing=auction_listing(Title=title,Description=description,Url=url,Tag=tag,date_time=datetime.now())
#                 print("test10")
#                 listing.User.add(u)
#                 print("test11")
#                 listing.save()
                
#                 # u.auction.add(listing)
#                 print(listing)
#                 print(datetime.now())
#                 # listing.save()
#                 return HttpResponseRedirect(reverse('index'))
#             except:
#                 print("test3")
                
#                 return render(request,"auctions/create.html",{
#                     "message":"An error occured try again",
#                     "form":create_form()
#                 })
#             print("test4")
#             return HttpResponseRedirect(reverse("index"))

#         print("test5")
#         return render(request,"auctions/create.html",{
#                     "message":"Check your inputs and try again",
#                     "form":create_form()
#                 })
#     print("test6")    
#     return render(request, "auctions/index.html",{
#         "listings":auction_listing.objects.all()
#     })




def index (request):
    if request.method == "POST":
        form=listing_form(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return render(request,"auctions/create.html",{
                "message":"Your Listing has been Succesfully Created.",
                "form":listing_form()
            })
            # messages.success(request, ('Your movie was successfully added!'))
        else:
            return render(request,"auctions/create.html",{
                "message":"OOPS!!,There was an error while saving your form ,try again.",
                "form":listing_form()
            })

    return render(request,"auctions/index.html",{
        "listings":auction_listing.objects.all()
    })
            

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


def create_listing(request):
    return render(request,"auctions/create.html",{
        "form":listing_form(),
    })