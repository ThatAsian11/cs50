from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("search", views.search, name="search"),
  path("trending", views.trending, name="trending"),
  path("content", views.content, name="content"),
  path("watchlist", views.watchlist, name="watchlist"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register")
]
