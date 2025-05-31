from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
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


def create_payment_intent(request, item_id):
    item = Item.objects.get(id=item_id)
    publishable_key = get_stripe_publishable_key()
    if not item:
        return JsonResponse({'error': 'Item not found'}, status=404)
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),  # Amount in cents
            currency=item.currency,
        )
        return JsonResponse({
            'clientSecret': intent.client_secret,
            'publishable_key': publishable_key
        })
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=403)


def payment_success(request):
    # This is where Stripe will redirect after payment
    return render(request, 'items/payment_success.html')
