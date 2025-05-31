from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:id>/', views.order_detail, name='order_detail'),
    path('buy/order/<int:id>/', views.buy_order, name='buy_order'),
    path('buy/item/<item_id>/', views.buy_item, name='buy_item'),
    path('create-payment-intent/order/<int:order_id>/', views.create_order_payment_intent, name='order_payment_intent'),
    path('create-payment-intent/item/<int:item_id>/', views.create_item_payment_intent, name='item_payment_intent'),
    path('payment-success/', views.payment_success, name='payment_success'),
]
