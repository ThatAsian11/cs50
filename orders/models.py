from django.db import models

# Create your models here.
# class Type(models.Model):
#     description = models.CharField(max_length=20)
#
#     def __str__(self):
#         return f" {self.id}: {self.order_on_menu}, {self.description}"
#
# class Topping(models.Model):
#     name = models.CharField(max_length = 32)
#
#     def __str__(self):
#         return f"{self.name}"
#
# class MenuItem(models.Model):
#     SIZE_CHOICES = (
#         ('S', 'Small'),
#         ('L', 'Large'),
#         ('', ''),
#     )
#     TOPPING_CHOICES =(
#
#         (0, 'No extra toppings'),
#         (1, '1 topping'),
#         (2, '2 toppings'),
#         (3, '3 toppings'),
#         (5, 'Special'),
#     )
#     OPTION_CHOICES =(
#         ('Y', 'Yes'),
#         ('N', 'No'),
#         ('C', 'Cheese-only'),
#     )
#     CRUST_CHOICES = (
#         ('S', 'Sicilian'),
#         ('R', 'Italian'),
#         ('', '')
#     )
#
#     type_new = models.ForeignKey(Type, on_delete=models.CASCADE, default=0, null=True)
#     name = models.CharField(max_length = 32)
#     options = models.CharField(max_length =1, choices= OPTION_CHOICES, default='N')
#     size = models.CharField(max_length=1, blank=True, choices=SIZE_CHOICES)
#     price = models.DecimalField(decimal_places=2, max_digits=5)
#     topping_cost = models.DecimalField(decimal_places=2, max_digits=3, default= 0.00)
#     number_of_toppings = models.SmallIntegerField(choices=TOPPING_CHOICES, default=0)
#     crust = models.CharField(max_length=1, blank=True, choices=CRUST_CHOICES, default='')
#
#     def __str__(self):
#         if ((self.type_new.description == 'Sicilian' or  self.type_new.description == 'Regular') and
#                 self.number_of_toppings == 0):
#             return f"{self.type_new.description}: {self.name}, {self.get_size_display()}, Cheese, Price: {self.price}"
#         if self.number_of_toppings == 0 and self.options != 'C':
#             return f"{self.type_new.description}: {self.name}, {self.get_size_display()}, Price: {self.price}"
#         else:
#             return f"{self.type_new.description}: {self.name}, {self.get_size_display()}, {self.get_number_of_toppings_display()}, Base Price: {self.price}"

class Pizza(models.Model):
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=32)
    small = models.DecimalField(decimal_places=2, max_digits=5)
    large = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['small']

class Topping(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Sub(models.Model):
    name = models.CharField(max_length=32)
    small = models.DecimalField(decimal_places=2, max_digits=5)
    large = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['large']

class DinnerPlatter(models.Model):
    name = models.CharField(max_length=32)
    small = models.DecimalField(decimal_places=2, max_digits=5)
    large = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['small']

class ElseItem(models.Model):
    type = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.name}"

class Cart(models.Model):
    order_id = models.IntegerField()
    type = models.CharField(max_length=32, null=True, blank=True, default=None)
    items = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return f"ID-{self.order_id},{self.type}: {self.items}"

class Order(models.Model):
    order_id = models.IntegerField()
    type = models.CharField(max_length=32)
    items = models.CharField(max_length=64)
    total = models.DecimalField(decimal_places=2, max_digits=8)
    date = models.CharField(max_length=20, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.items} : {self.total}"

    class Meta:
        ordering = ['order_id']
