from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('confirm-order-payment/', views.confirm_order_payment, name='confirm_order_payment'),

]
