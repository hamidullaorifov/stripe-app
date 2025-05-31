from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from items.models import Item, Currency


class Discount(models.Model):
    name = models.CharField(max_length=50)
    percent_off = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    stripe_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"


class Tax(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.FloatField(validators=[MinValueValidator(0)])
    inclusive = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_completed = models.BooleanField(default=False)

    def get_total_amount(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total *= (1 - self.discount.percent_off / 100)
        return round(total, 2)

    def get_currency(self):
        currencies = set(item.currency for item in self.items.all())
        if len(currencies) == 1:
            return currencies.pop()
        return Currency.USD  # default if multiple currencies

    def __str__(self):
        return f"Order #{self.id}"
