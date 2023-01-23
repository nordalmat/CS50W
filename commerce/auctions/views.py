from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import random

from .models import User, Brand, AuctionListing, Comment, Bid


def random_selection(size):
    try:
        k = random.sample(range(0, size), 5)
        selection = []
        all_entries = AuctionListing.objects.filter(isActive=True).all()
        for idx in k:
            selection.append(all_entries[idx])
        return selection
    except ValueError:
        print('Sample size exceeded population size.')


def index(request):
    allAuctions = AuctionListing.objects.filter(isActive=True).all()
    allBrands = Brand.objects.all()
    return render(request, "auctions/index.html", {
        'auctions': allAuctions, 
        'brands': allBrands, 
        'activate': True
    })


def create_listing(request):
    if request.method == "GET":
        allBrands = Brand.objects.all()
        return render(request, 'auctions/new.html', {
            'brands': allBrands
        })
    else:
        user = request.user
        title = request.POST['title']
        price = request.POST['price']
        bid = Bid(amount=float(price), user=user)
        bid.save()
        imageurl = request.POST['imageurl']
        description = request.POST['description']
        brand = request.POST['brand']
        brand_data = Brand.objects.get(name=brand)
        new = AuctionListing(
            title=title, price=bid,
            image_url=imageurl, description=description,
            author=user, brand=brand_data
        )
        new.save()
        return HttpResponseRedirect(reverse('auctions:index'))


def brands(request):
    allBrands = Brand.objects.all()
    return render(request, 'auctions/brands.html', {
        'allBrands': allBrands, 
        'msg': 'There is no available brands.'
    })


def list_filter(request):
    if request.method == 'POST':
        select = request.POST['brand']
        if select == 'All brands':
            brand = Brand.objects.all()
            allAuctions = AuctionListing.objects.filter(isActive=True).all()
        else:
            brand = Brand.objects.get(name=select)
            allAuctions = AuctionListing.objects.filter(isActive=True, brand=brand).all()
        if len(allAuctions) == 0:
            msg = 'Currently, there is no listings of a particular brand.'
        else:
            msg = None
        allBrands = Brand.objects.all()
        return render(request, "auctions/index.html", {
            'auctions': allAuctions, 
            'brands': allBrands,
            'msg': msg,
            'activate': True
        })


def brand_entries(request, id):
    allAuctions = AuctionListing.objects.filter(isActive=True, brand=id).all()
    if len(allAuctions) == 0:
        msg = 'Currently, there is no listings of a particular brand.'
    else:
        msg = None
    allBrands = Brand.objects.all()
    return render(request, "auctions/index.html", {
            'auctions': allAuctions, 
            'brands': allBrands,
            'msg': msg,
            'activate': True
        })


def listing(request, id):
    entry = get_object_or_404(AuctionListing, id=id)
    entry_in_watchlist = request.user in entry.watchlist.all()
    all_comments = Comment.objects.filter(listing=entry).all()
    if len(all_comments) == 0:
        msg = 'No comments yet. Be the first one to comment...'
    else:
        msg = None
    isOwner = request.user.username == entry.author.username
    selection = random_selection(len(AuctionListing.objects.filter(isActive=True).all()))
    return render(request, 'auctions/listing.html', {
        'entry': entry,
        'entry_in_watchlist': entry_in_watchlist,
        'all_comment': all_comments,
        'msg': msg, 
        'isOwner': isOwner, 
        'selection': selection, 
        'isNotActive': 'This auction is not longer active.'
    })


def remove_watchlist_on_listing_page(request, id):
    listing_data = AuctionListing.objects.get(pk=id)
    user = request.user
    listing_data.watchlist.remove(user)
    return HttpResponseRedirect(reverse('auctions:listing', args=(id,)))


def remove_entry_in_watchlist(request, id):
    listing_data = AuctionListing.objects.get(pk=id)
    user = request.user
    listing_data.watchlist.remove(user)
    return HttpResponseRedirect(reverse('auctions:watchlist'))


def add_watchlist(request, id):
    listing_data = AuctionListing.objects.get(pk=id)
    user = request.user
    listing_data.watchlist.add(user)
    return HttpResponseRedirect(reverse('auctions:listing', args=(id,)))


def view_watchlist(request):
    user = request.user
    all_listing_data = user.itemlist.all()
    allBrands = Brand.objects.all()
    if len(all_listing_data) == 0:
        msg = 'Your Watchlist is empty.'
    else: msg = None
    return render(request, 'auctions/watchlist.html', {
        'all_listing_data': all_listing_data,
        'allBrands': allBrands, 
        'msg': msg
    })


def add_comment(request, id):
    if request.method == 'POST':
        user = request.user
        listing_data = AuctionListing.objects.get(pk=id)
        content = request.POST.get('comment')
        new_comment = Comment(
            listing=listing_data,
            author=user, 
            content=content)
        new_comment.save()
        return HttpResponseRedirect(reverse('auctions:listing', args=(id,)))


def make_bid(request, id):
    if request.method == 'POST':
        user = request.user
        entry = AuctionListing.objects.get(pk=id)
        bid = float(request.POST['bid'])
        all_comments = Comment.objects.filter(listing=entry).all()
        selection = random_selection(len(AuctionListing.objects.filter(isActive=True).all()))
        isOwner = request.user.username == entry.author.username
        if len(all_comments) == 0:
            msg = 'No comments yet. Be the first one to comment...'
        else:
            msg = None
        if bid > float(entry.price.amount):
            new_bid = Bid(
                user=user,
                amount=bid
            )
            new_bid.save()
            entry.price = new_bid
            entry.save()
            return render(request, 'auctions/listing.html', {
                'entry': entry,
                'bid_msg': 'Your bid was accepted.', 
                'success': True,
                'all_comment': all_comments,
                'isOwner': isOwner, 
                'selection': selection, 
                'msg': msg,
                'isNotActive': 'This auction is not longer active.'
            })
        else:
            return render(request, 'auctions/listing.html', {
                'entry': entry,
                'bid_msg': 'Your bid must be higher than the current bid!', 
                'success': False,
                'all_comment': all_comments,
                'isOwner': isOwner, 
                'selection': selection, 
                'msg': msg,
                'isNotActive': 'This auction is not longer active.'

            }) 


def close_listing(request, id):
    entry = AuctionListing.objects.get(id=id)
    entry.isActive = False
    entry.save()

    entry_in_watchlist = request.user in entry.watchlist.all()
    isOwner = request.user.username == entry.author.username
    all_comments = Comment.objects.filter(listing=entry).all()
    if len(all_comments) == 0:
        msg = 'No comments yet. Be the first one to comment...'
    else:
        msg = None
    selection = random_selection(len(AuctionListing.objects.filter(isActive=True).all()))

    return render(request, 'auctions/listing.html', {
        'entry': entry,
        'entry_in_watchlist': entry_in_watchlist,
        'all_comment': all_comments,
        'msg': msg, 
        'isOwner': isOwner, 
        'selection': selection, 
        'success': True, 
        'closing_msg': 'Your auction was closed successfully.',
        'isNotActive': 'This auction is not longer active.'
    })


def users(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'auctions/users.html', {
        'user': user
    })


def user_entries(request, id):
    allAuctions = AuctionListing.objects.filter(isActive=True, author=id).all()
    if len(allAuctions) == 0:
        msg = 'Currently, there is no listings from a particular user.'
    else:
        msg = None
    allBrands = Brand.objects.all()
    return render(request, "auctions/index.html", {
            'auctions': allAuctions, 
            'brands': allBrands,
            'msg': msg
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
