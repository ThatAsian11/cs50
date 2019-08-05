import time
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from helpers import Search, Trending
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import Watchlist

# Create your views here.
def index(request):
    # Updates the status of an item in the watchlist
    if request.method == 'POST':
        id = request.POST.get('content_id')
        Watchlist.objects.filter(content_id=id).update(watched=True)
        return redirect('watchlist')
    # Renders Home page
    else:
        return render(request, "watchlist/index.html")

def search(request):
    # Passes the query to search function and returns JSON response
    if request.method == 'POST':
        print("received")
        a = request.POST.get('search_query')
        query = Search.all_search(a)
        # If search fails or there are no matches to query, alert user
        if query == None or query['total_results'] == 0:
            error = True
            context = {
            "error": error
            }
            return render(request, "watchlist/search.html", context)
        
        # Renders search results otherwise
        else:
            context = {
            "items": query['results']
            }
            return render(request, "watchlist/search.html", context)
    else:
        return render(request, "watchlist/search.html")

def trending(request):
    # Returns the weekly trending movie or show
    if request.method == 'POST':
        trend = request.POST.get('trend')
        # Returns movie trends
        if trend == 'movie':
            data = Trending.Weekly.movie_trend()
            # Returns error message if trending request fails
            if data == None:
                error = True
                context = {
                "error": error
                }
                return render(request, "watchlist/index.html", context)
            # Renders trending movies otherwise
            else:
                context = {
                "items": data['results'],
                "movie": True
                }
                return render(request, "watchlist/trending.html", context)
        elif trend == 'tv':
            data = Trending.Weekly.tv_trend()
            # Returns error message if trending request fails
            if data == None:
                error = True
                context = {
                "error": error
                }
                return render(request, "watchlist/index.html", context)
            # Renders trending shows otherwise
            else:
                context = {
                "items": data['results'],
                "movie": False
                }
                return render(request, "watchlist/trending.html", context)
    # Render trending movies by default
    else:
        data = Trending.Weekly.movie_trend()
        # Returns error message if trending request fails
        if data == None:
            error = True
            context = {
            "error": error
            }
            return render(request, "watchlist/index.html", context)
        # Render movies otherwise
        else:
            context = {
            "items": data['results'],
            "movie": True
            }
            return render(request, "watchlist/trending.html", context)

def content(request):
    # Only show content data after user clicks on info button and submits content id
    if request.method == 'POST':
        media = request.POST.get('content')
        id = request.POST.get('content_id')
        check = Watchlist.objects.filter(content_id=id)
        added = False
        # If check exists, the item has already been added to watchlist so renders a tick mark instead of button
        if check:
            added = True
        if media == 'movie':
            data = Search.movie_find(id)
            context = {
            "items": data,
            "added": added
            }
            return render(request, "watchlist/content.html", context)
        elif media == 'tv':
            data = Search.tv_find(id)
            context = {
            "items": data,
            "added": added
            }
            return render(request, "watchlist/content.html", context)
    # Redirects user to home page if /content is accessed directly
    else:
        return redirect('index')

def watchlist(request):
    # Only allow addition to watchlist if user is logged in
    if request.user.is_authenticated:
        user_id = request.user.id
        datetime = time.strftime('%H:%M:%S on %d/%m/%y')
        data = Watchlist.objects.filter(profile_id=user_id)
        # Adds item to watchlist
        if request.method == "POST":
            title = request.POST.get('content_title')
            media_id = request.POST.get('content_id')
            media_type = request.POST.get('content_type')
            print(title, id)
            a = Watchlist(profile_id=user_id, content_id=media_id, type=media_type, title=title, date=datetime)
            a.save()
            return redirect("watchlist")
        # Displays all the items in the watchlist
        else:
            context = {
            "items": data
            }
            return render(request, "watchlist/watchlist.html", context)
    # Sends user to log in page if addition to watchlist is attempted
    else:
        return render(request, "watchlist/login.html", {"message": "Please log in to add items to watchlist"})

def register(request):
    # Register users with data from form
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    # Dislaying Registration form
    else:
        form = SignUpForm()
    return render(request, "watchlist/register.html", {'form': form})

def login_view(request):
    # Logging in user using built in method
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("index")
    else:
        return render(request, "watchlist/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    # logging out user using built in method
    logout(request)
    return render(request, "watchlist/login.html", {"message": "Logged out."})
