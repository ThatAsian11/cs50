from django.contrib import admin
from .models import Pizza, Topping, Sub, DinnerPlatter, ElseItem, Cart, Order

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(DinnerPlatter)
admin.site.register(ElseItem)
admin.site.register(Cart)
admin.site.register(Order)
