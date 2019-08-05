from django.shortcuts import render
from django.http import HttpResponse
from helpers import Search, Trending

# Create your views here.
def index(request):
    return render(request, "watchlist/index.html")
def search(request):
    if request.method == 'POST':
        print("received")
        q = request.POST.get('search_query')
        q = q.strip()
        q = [i.replace(' ', '+') for i in q]
        a = ''.join(q)
        print(a)
        query = Search.all_search(a)
        # print(query)
        context = {
        "items": query['results']
        }
        return render(request, "watchlist/search.html", context)
    else:
        return render(request, "watchlist/search.html")

def trending(request):
    if request.method == 'POST':
        trend = request.POST.get('trend')
        print(trend)
        if trend == 'movie':
            data = Trending.Weekly.movie_trend()
            context = {
            "items": data['results']
            }
            return render(request, "watchlist/trending.html", context)
        elif trend == 'tv':
            data = Trending.Weekly.tv_trend()
            context = {
            "items": data['results']
            }
            return render(request, "watchlist/trending.html", context)
    else:
        data = Trending.Weekly.movie_trend()
        context = {
        "items": data['results']
        }
        return render(request, "watchlist/trending.html", context)
