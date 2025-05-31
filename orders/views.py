from django.shortcuts import get_object_or_404, render
import stripe
from django.conf import settings
from django.http import JsonResponse
from .models import Order
from items.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': item.currency.lower(),
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': int(item.price * 100),  # Convert to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/payment-success/'),
                cancel_url=request.build_absolute_uri('/'),
            )

            return JsonResponse({
                'session': session.id,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)

    context = {
        'order': order,
        'items': order.items.all(),
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_currency': order.get_currency().upper(),
    }

    if order.discount:
        context['discount_amount'] = sum(
            item.price for item in order.items.all()
        ) * (order.discount.percent_off / 100)

    if order.tax and not order.tax.inclusive:
        subtotal = sum(item.price for item in order.items.all())
        if 'discount_amount' in context:
            subtotal -= context['discount_amount']
        context['tax_amount'] = subtotal * (order.tax.percentage / 100)

    return render(request, 'orders/order_detail.html', context)


def buy_order(request, id):
    order = get_object_or_404(Order, pk=id)
    currency = order.get_currency()
    line_items = []
    for item in order.items.all():
        line_item = {
            'price_data': {
                'currency': currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),  # convert to cents
            },
            'quantity': 1,
        }

        # Apply tax if exists
        if order.tax:
            line_item['tax_rates'] = [order.tax.stripe_id]

        line_items.append(line_item)

    discounts = []
    if order.discount:
        discounts.append({
            'coupon': order.discount.stripe_id or None
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            discounts=discounts,
            success_url=request.build_absolute_uri('/payment-success/'),
            cancel_url=request.build_absolute_uri('/'),
        )
        return JsonResponse({'session': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def create_order_payment_intent(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(order.get_total_amount() * 100),
            currency=order.get_currency(),
            metadata={'order_id': order.id},
        )
        return JsonResponse({
            'clientSecret': intent['client_secret'],
            'amount': intent['amount'],
            'currency': intent['currency']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def create_item_payment_intent(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),
            currency=item.currency,
            metadata={'item_id': item.id},
        )
        return JsonResponse({
            'clientSecret': intent['client_secret'],
            'amount': intent['amount'],
            'currency': intent['currency']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def payment_success(request):
    # This is where Stripe will redirect after payment
    return render(request, 'orders/payment_success.html')
