from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('item/<int:id>/', views.get_item, name='item_detail'),
    # path('create-payment-intent/<int:item_id>/', views.create_payment_intent, name='create_payment_intent'),
    path('payment-success/', views.payment_success, name='payment_success'),
]
