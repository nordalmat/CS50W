import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like


def index(request, username=None):
    all_likes = Like.objects.all()
    liked_posts = []
    for like in all_likes:
        if like.user.id == request.user.id:
            liked_posts.append(like.post.id)

    if username is None:
        all_posts = Post.objects.order_by('-timestamp').all()
        
        #Pagination
        paginator = Paginator(all_posts, 5)
        page_number = request.GET.get('page')
        page_posts = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            'page_posts': page_posts,
            'liked_posts': liked_posts
        })
    else:
        user = User.objects.get(username=username)
        user_posts = Post.objects.order_by('-timestamp').filter(author=user.id).all()
        following = Follow.objects.filter(user=user)
        followers = Follow.objects.filter(following=user)
    
        #Pagination
        paginator = Paginator(user_posts, 5)
        page_number = request.GET.get('page')
        page_posts = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            'page_posts': page_posts, 
            'username': username,
            'following': following,
            'followers': followers, 
            'is_following': request.user.username in [u.user.username for u in followers],
            'profile': user,
            'liked_posts': liked_posts
        })


def following(request):
    current_user = User.objects.get(id=request.user.id)
    follows = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.order_by('-timestamp').all()

    relevant_posts = []
    for post in all_posts:
        for follow in follows:
            if follow.following == post.author:
                relevant_posts.append(post)
    
    all_likes = Like.objects.all()
    liked_posts = []
    for like in all_likes:
        if like.user.id == request.user.id:
            liked_posts.append(like.post.id)

    #Pagination
    paginator = Paginator(relevant_posts, 5)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        'page_posts': page_posts,
        'liked_posts': liked_posts
    })


def edit(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    edit_post = Post.objects.get(id=id)
    text_body = data.get('body')
    if text_body == '':
        return JsonResponse({
            'error': 'Text cannot be none.'
        })
    edit_post.body = text_body
    edit_post.save()
    return JsonResponse({'message': 'Post saved successfylly.', 'content': edit_post.body}, status=201)


@csrf_exempt
@login_required
def new_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    text_body = data.get('body')
    if text_body == '':
        return JsonResponse({
            'error': 'Text cannot be none.'
        })
    
    post = Post(
        author = request.user,
        body = text_body
    )
    post.save()
    return JsonResponse({'message': 'Post saved successfylly.'}, status=201)


def follow(request):
    username_to_follow = request.POST['user_to_follow']
    user_to_follow = User.objects.get(username=username_to_follow)
    current_user = User.objects.get(id=request.user.id)
    follow = Follow(user=current_user, following=user_to_follow)
    follow.save()
    return HttpResponseRedirect(reverse(index, kwargs={'username': user_to_follow.username}))


def unfollow(request):
    username_to_follow = request.POST['user_to_follow']
    user_to_follow = User.objects.get(username=username_to_follow)
    current_user = User.objects.get(id=request.user.id)
    unfollow = Follow.objects.get(user=current_user, following=user_to_follow)
    unfollow.delete()
    return HttpResponseRedirect(reverse(index, kwargs={'username': user_to_follow.username}))


def add_like(request, id):
    post = Post.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    like = Like(user=user, post=post)
    like.save()
    return JsonResponse({'message': 'Post liked successfylly.'}, status=201)


def remove_like(request, id):
    post = Post.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({'message': 'Like removed successfylly.'}, status=201)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
