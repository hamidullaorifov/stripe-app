from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from items.models import Item, Currency
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class Discount(models.Model):
    name = models.CharField(max_length=50)
    percent_off = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        max_digits=4,
        decimal_places=2)
    stripe_id = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if this is a new instance
        super().save(*args, **kwargs)

        if is_new or not self.stripe_id:
            self.create_stripe_coupon()

    def create_stripe_coupon(self):
        stripe_coupon = stripe.Coupon.create(
            percent_off=float(self.percent_off),
            duration="once",
            name=self.name
        )
        self.stripe_id = stripe_coupon.id
        self.save(update_fields=['stripe_id'])

    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"


class Tax(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.DecimalField(validators=[MinValueValidator(0)], max_digits=4, decimal_places=2)
    inclusive = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new or not self.stripe_id:
            self.create_stripe_tax_rate()

    def create_stripe_tax_rate(self):
        stripe_tax_rate = stripe.TaxRate.create(
            display_name=self.name,
            percentage=float(self.percentage),
            inclusive=self.inclusive
        )
        self.stripe_id = stripe_tax_rate.id
        self.save(update_fields=['stripe_id'])

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

    def get_total_amount(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total *= (1 - self.discount.percent_off / 100)
        if self.tax:
            total *= (1 + self.tax.percentage / 100)
        return round(total, 2)

    def get_currency(self):
        currencies = set(item.currency for item in self.items.all())
        if len(currencies) == 1:
            return currencies.pop()
        return Currency.USD  # default if multiple currencies

    def __str__(self):
        return f"Order #{self.id}"


def sync_stripe_discounts():
    # Sync discounts
    for discount in Discount.objects.filter(stripe_id__isnull=True):
        stripe_coupon = stripe.Coupon.create(
            percent_off=float(discount.percent_off),
            duration="once",
            name=discount.name
        )
        discount.stripe_id = stripe_coupon.id
        discount.save()


def sync_stripe_taxes():
    for tax in Tax.objects.filter(stripe_id__isnull=True):
        stripe_tax_rate = stripe.TaxRate.create(
            display_name=tax.name,
            percentage=float(tax.percentage),
            inclusive=tax.inclusive
        )
        tax.stripe_id = stripe_tax_rate.id
        tax.save()
