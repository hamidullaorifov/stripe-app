from django.shortcuts import get_object_or_404
import json
import stripe
from .models import Order
from items.models import Item


def buy_items(request):
    body = json.loads(request.body)
    items_list = body.get('items', [])
    items = (get_object_or_404(Item, pk=item.get('id')) for item in items_list)
    Order.objects.create(items=items)
    currency = items[0].currency if items else 'usd'
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            } for item in items
        ],
        mode='payment',
        success_url='https://youtube.com',
        cancel_url='https://google.com',
    )
    return JsonResponse({'session': session})
