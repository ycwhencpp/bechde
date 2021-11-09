from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User, auction_listing,comments,bids
from .forms import listing_form,bid_form,comment_form

from django.contrib.auth.decorators import login_required
from django.contrib import messages





def index (request):

    return render(request,"auctions/index.html",{
        "listings":auction_listing.objects.filter(active=True).all()
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
            messages.error(request,"Invalid username and/or password.")
            return render(request, "auctions/login.html")
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
            messages.error(request, 'Passwords Must Match.')
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request,"Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login")
def create_listing(request):
    if request.method == "POST":
        form=listing_form(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request,"Listing succesfully created.")
            return redirect("/")

        else:
            messages.error(request,"Oops!! an error occured while saving ,Try again.")
            return HttpResponseRedirect(reverse('create'))

    return render(request,"auctions/create.html",{
        "form":listing_form(),
    })



def view_listing(request,id):
    listing=auction_listing.objects.get(pk=id)

    if request.user.is_authenticated:
        is_in_watchlist=listing.is_in_watchlist(request.user)
    else:
        is_in_watchlist=False
    
    if auction_listing.objects.get(pk=id).active==False:
        messages.info(request,"auction has been closed")

    if listing.bid.count()>0:
        current_winner=listing.bid.get(amount=listing.current_bid).user
        
    else:
        current_winner=False
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "bid_form":bid_form,
        "max_bid":listing.current_bid,
        "comment_form":comment_form,
        "comments":comments.objects.filter(listing=id).all(),
        "comment_count":comments.objects.filter(listing=id).all().count(),
        "count":bids.objects.filter(listing=id).all().count(),
        "is_in_watchlist":is_in_watchlist,
        "current_winner":current_winner,
        
    })

@login_required(login_url="/login")
def place_bid(request,id):

    if request.method=="POST":
        bidform=bid_form(request.POST)
        a=auction_listing.objects.get(pk=id)
        if bidform.is_valid():
                    
            bidform.instance.user=request.user
            bidform.instance.listing=a
            current_bid=bidform.cleaned_data["amount"]
            if int(current_bid) > auction_listing.objects.get(pk=id).current_bid:
                bidform.save()
                messages.success(request, 'Bid successfully added.')

                return HttpResponseRedirect(reverse('listing',args=[id]))
            else:
                messages.info(request, 'Place Bid higher then Current bid.')

        else:
            messages.error(request, 'We are not able to add your bid please try again.')
            return HttpResponseRedirect(reverse('listing',args=[id]))
                
    return HttpResponseRedirect(reverse('listing',args=[id]))
        

@login_required(login_url='/login')
def close_bid(request,id):
    if request.method=="POST" and request.user == auction_listing.objects.get(pk=id).author :

        listing=auction_listing.objects.get(pk=id)
        # bid=bids.objects.filter(listing=listing).all()
        # max=bid.aggregate(Max('amount'))['amount__max']
        max=listing.current_bid
        print(max)
        print(listing.author)
        # if listing.bid.all() ==0:
        #     print(listing.bid.all())
        #     user=request.user
        # user=bids.objects.get(amount=max).user

        # print(t)
        # print(t.listing)
        # print(t.user)
        # print(x)
        if listing.bid.count()>0:
            current_winner=listing.bid.get(amount=listing.current_bid).user
        else:
            current_winner=False
        listing.active=False
        listing.save()
        messages.success(request, 'Auction Succesfully Closed.')
            
        return render(request,"auctions/listing.html",{
        # "bid_winner":user,
        "listing":auction_listing.objects.get(pk=id),
        "bid_form":bid_form,
        "max_bid":auction_listing.objects.get(pk=id).current_bid,
        "comment_form":comment_form,
        "comments":comments.objects.filter(listing=id).all(),
        "count":bids.objects.filter(listing=id).all().count(),
        "comment_count":comments.objects.filter(listing=id).all().count(),
        "current_winner":current_winner,
        })
    
    return HttpResponseRedirect(reverse('listing',args=[id]))



@login_required(login_url="/login")
def place_comment(request,id):
    if request.method=="POST":
        commentform=comment_form(request.POST)
        if commentform.is_valid():
            commentform.instance.author=request.user
            commentform.instance.listing=auction_listing.objects.get(pk=id)
            commentform.save()
            messages.success(request, 'comment sucessfully added.')
            return HttpResponseRedirect(reverse('listing',args=[id]))
        else:
            messages.error(request, 'We are not able to add your comment please try again.')
            return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(reverse('listing',args=[id]))




@login_required(login_url="/login") 
def update_watchlist(request,id):
    if request.method=="POST":
        user=request.user
        listing=auction_listing.objects.get(pk=id)
        if listing in  auction_listing.objects.filter(is_watched=request.user).all(): # or listing.is_in_watchlist(user)
            listing.is_watched.remove(user)
            messages.info(request, 'removed from watchlist')
        else:
            listing.is_watched.add(user)
            messages.info(request, 'added to watchlist')
    return HttpResponseRedirect(reverse('listing',args=[id]))
    

@login_required(login_url='/login')
def remove_watchlist(request,id):
    if request.method=="POST":

        listing=auction_listing.objects.get(pk=id)

        user=request.user

        # user.watchlist.remove(listing)
        listing.is_watched.remove(user)

        messages.success(request,"Removed from Watchlist.")
    return HttpResponseRedirect(reverse('watchlist'))


@login_required(login_url="/login") 
def watchlist(request):
    return render(request,'auctions/watchlist.html',{
        "watchlist":auction_listing.objects.filter(is_watched=request.user).all()
    })

def categories(request):

    return render(request,"auctions/categories.html",{
        "categories":set(auction_listing.objects.values_list("Tag",flat=True))
    })

def view_category(request,category):
    listing=auction_listing.objects.filter(Tag=category).all()
    categories=set(auction_listing.objects.values_list("Tag",flat=True))

    if category not in categories:
        messages.error(request,f"No listing found in the category of {category}.")
        return HttpResponseRedirect(reverse('categories'))

    return render(request,"auctions/view_category.html",{
        "listing":listing.filter(active=True).all(),
        "tag":category
    })