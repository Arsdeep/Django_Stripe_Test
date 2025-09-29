from django.shortcuts import render, redirect
from django.conf import settings
from .models import Product, Order, OrderItem
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def shop_home(request):
    products = Product.objects.all()
    orders = Order.objects.filter(paid=True)
    return render(request, 'shop/home.html', {
        'products': products,
        'orders': orders,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        # Get products and quantities from POST
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')

        # Create an order
        order = Order.objects.create(paid=False)

        total_amount = 0
        for pid, qty in zip(product_ids, quantities):
            product = Product.objects.get(id=pid)
            qty = int(qty)
            OrderItem.objects.create(order=order, product=product, quantity=qty)
            total_amount += product.price * qty

        # Create Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100),
            currency='usd',
        )
        order.stripe_payment_intent = intent['id']
        order.save()

        return render(request, 'shop/checkout.html', {
            'client_secret': intent['client_secret'],
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'order_id': order.id
        })
    return redirect('shop_home')


@csrf_exempt
def stripe_success(request):
    # Optional endpoint if you want to confirm payment later
    return redirect('shop_home')

@csrf_exempt
def confirm_order_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)

        # Retrieve the PaymentIntent from Stripe to verify status
        intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent)

        if intent.status == 'succeeded':
            order.paid = True
            order.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})