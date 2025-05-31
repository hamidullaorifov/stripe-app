from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Item
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_stripe_publishable_key():
    return settings.STRIPE_PUBLISHABLE_KEY


def index(request):
    items = Item.objects.all()
    publishable_key = get_stripe_publishable_key()
    return render(request, 'items/index.html', {'items': items, 'stripe_publishable_key': publishable_key})


def get_item(request, id):
    item = get_object_or_404(Item, pk=id)
    publishable_key = get_stripe_publishable_key()
    return render(request, 'items/item_detail.html', {'item': item, 'stripe_publishable_key': publishable_key})
