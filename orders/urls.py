from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:id>/', views.order_detail, name='order_detail'),
    path('buy/order/<int:id>', views.buy_order, name='buy_order'),
    path('buy/item/<item_id>/', views.buy_item, name='buy_item'),
    path('create-payment-intent/<int:order_id>', views.create_payment_intent, name='create_payment_intent')
]
