from django.db import models

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
