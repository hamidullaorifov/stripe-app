from django.db import models


class Currency(models.TextChoices):
    USD = 'usd', 'US Dollar'
    EUR = 'eur', 'Euro'


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )

    def __str__(self):
        return f"{self.name} ({self.get_currency_display()})"
