from django.shortcuts import render, redirect
from django.conf import settings
from .models import Product, Order, OrderItem
import stripe
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY

def shop_home(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, paid=True)
    else:
        orders = Order.objects.none()  # no orders for anonymous users

    return render(request, 'shop/home.html', {
        'products': products,
        'orders': orders,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


@login_required(login_url='login')
def create_checkout_session(request):
    if request.method == 'POST':

        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')

        # Build cart items and compute total.
        cart_items = []
        total_amount = 0
        for pid, qty in zip(product_ids, quantities):
            qty_int = int(qty)
            if qty_int <= 0:
                continue
            product = Product.objects.get(id=pid)
            cart_items.append({
                'product_id': str(product.id),
                'quantity': qty_int,
            })
            total_amount += product.price * qty_int

        if total_amount == 0:
            return redirect('shop_home')

        # Created Stripe PaymentIntent with cart metadata to reconstruct later
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100), # *100 to convert dollars to cents
            currency='usd',
            metadata={
                'cart': json.dumps(cart_items),
                'user_id': str(request.user.id),
                'username': request.user.username,
            },
        )

        return render(request, 'shop/checkout.html', {
            'client_secret': intent['client_secret'],
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'payment_intent_id': intent['id'],
        })
    return redirect('shop_home')


@login_required(login_url='login')
def confirm_order_payment(request):
    if request.method == 'POST':

        payment_intent_id = request.POST.get('payment_intent_id')
        if not payment_intent_id:
            return JsonResponse({'status': 'failed', 'reason': 'missing_payment_intent'}, status=400)

        try:
            # Retrievs the PaymentIntent from Stripe
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        except stripe.error.StripeError as e:
            return JsonResponse({'status': 'failed', 'reason': str(e)}, status=400)

        if intent.status == 'succeeded':
            cart_json = getattr(intent, 'metadata', {}).get('cart', '[]')
            try:
                cart_items = json.loads(cart_json)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'failed', 'reason': 'invalid_cart_data'}, status=400)

            if not cart_items:
                return JsonResponse({'status': 'failed', 'reason': 'empty_cart'}, status=400)

            order = Order.objects.create(
                user=request.user,
                paid=True,
                stripe_payment_intent=payment_intent_id
            )

            for item in cart_items:
                pid = item.get('product_id')
                qty = int(item.get('quantity', 0))
                if not pid or qty <= 0:
                    continue
                try:
                    product = Product.objects.get(id=pid)
                except Product.DoesNotExist:
                    continue
                OrderItem.objects.create(order=order, product=product, quantity=qty)

            return JsonResponse({'status': 'success'}, status=200)

        return JsonResponse({'status': 'failed', 'reason': 'payment_not_succeeded'}, status=400)

    return JsonResponse({'status': 'failed', 'reason': 'invalid_method'}, status=405)