from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("order", views.order, name="order"),
    path("cart", views.cart, name="cart"),
    path('process', views.process, name="process"),
    path('placed', views.placed, name="placed"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]
