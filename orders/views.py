from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import SignUpForm
from .models import Pizza, Sub, Topping, DinnerPlatter, ElseItem, Cart, Order
from decimal import Decimal
import time
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "orders/login.html", {"message": None})
    return render(request, "orders/index.html")

def order(request):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "orders/login.html", {"message": None})
    # Getting all items from database
    pizza = Pizza.objects.all()
    topping = Topping.objects.all()
    sub = Sub.objects.all()
    sub_top = Topping.objects.filter(pk__in=[3,4,10])
    platter = DinnerPlatter.objects.all()
    rest = ElseItem.objects.all()
    # Sending all items to template
    context = {
        "user": request.user,
        "pizzas": pizza,
        "toppings": topping,
        "subs": sub,
        "subtops": sub_top,
        "platters": platter,
        "items": rest
    }
    return render(request, "orders/order.html", context)

def process(request):
    user_id = request.user.id
    if not request.user.is_authenticated:
        # display login form
        return render(request, "orders/login.html", {"message": None})

    # Get entered item from order form
    pizza = request.POST.get('pizza_selection')
    topping = request.POST.getlist('topping_selection')
    sub = request.POST.get('sub_selection')
    subtopping = request.POST.get('subtop_selection')
    item = request.POST.get('item_selection')
    platter = request.POST.get('platter_selection')

    # Adding any selected items to database with toppings/extras
    if pizza is not None:
        pizza_choice = Pizza.objects.get(pk=int(pizza))
        type = pizza_choice.type
        size = request.POST.get('size_choice')
        if topping is not None:
            items = 'Pizza ' + pizza_choice.name + '; ' + 'Topping: '
            topping_choices = Topping.objects.filter(pk__in=topping)
            for topp in topping_choices:
                items += topp.name + ' '
            if size == "small":
                price = pizza_choice.small
            else:
                price = pizza_choice.large
        else:
            if size == "small":
                price = pizza_choice.small
            else:
                price = pizza_choice.large
            items = 'Pizza ' + pizza_choice.name
        print(items)
        print(price)
    if sub is not None:
        sub_choice = Sub.objects.get(pk=int(sub))
        type = 'Sub'
        size = request.POST.get('size_choice')
        if subtopping is not "":
            subtop_choice = request.POST.get('subtop_selection')
            subtopp = Topping.objects.get(pk=subtop_choice)
            items = sub_choice.name + "; " + subtopp.name
            if size == 'small':
                price = float(sub_choice.small)
            else:
                price = float(sub_choice.large)
            price += 0.5
        else:
            size = request.POST.get('size_choice')
            if size == 'small':
                price = float(sub_choice.small)
            else:
                price = float(sub_choice.large)

            items = sub_choice.name
        extra = request.POST.get('extra_cheese')
        if extra == "true":
            price += 0.50
        print(items)
        print(price)

    if item is not None:
        item_choice = ElseItem.objects.get(pk=item)
        type = item_choice.type
        items = item_choice.name
        price = item_choice.price
        print(items)
        print(price)

    if platter is not None:
        platter_choice = DinnerPlatter.objects.get(pk=platter)
        type = "Platter"
        items = 'Dinner Platter: ' + platter_choice.name
        size = request.POST.get('size_choice')
        if size == 'small':
            price = platter_choice.small
        else:
            price = platter_choice.large
        print(items)
        print(price)

    p = Cart(order_id=user_id,type=type, items=items, price=price)
    p.save()
    return redirect('cart')
def cart(request):
    user_id = request.user.id
    selection = Cart.objects.filter(order_id=user_id)
    total = selection.aggregate(Sum('price'))['price__sum']

    # If order confirmed, add order to database, clear cart and send confirmation email
    if request.method == 'POST':
        order_datetime = time.strftime('%H:%M:%S on %d/%m/%y')
        username = request.user.username
        for item in selection:
            o = Order(order_id=user_id, type=item.type, items=item.items, total=item.price, date=order_datetime)
            o.save()
        selection.delete()
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        confirmation = EmailMessage('Order Confirmation', 'Your order has been confirmed!', to=[user.email])
        confirmation.send()
        print(user.email)
        prompt = True
        context = {
        "confirmation" : prompt
        }
        return render(request, "orders/index.html", context)
    # Show all items in cart
    else:
        context = {
        "items": selection,
        "subtotal": total
        }
        return render(request, "orders/cart.html", context)
def placed(request):
    # Getting all placed orders and passing to template
    orders = Order.objects.all()
    print(orders)
    context = {
    "orders": orders
    }
    # Erase past orders if orders are cleared by staff
    if request.method == "POST":
        orders.delete()
    return render(request, "orders/placed.html", context)

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
    return render(request, "orders/register.html", {'form': form})

def login_view(request):
    # Logging in user using built in method
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    # logging out user using built in method
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})
