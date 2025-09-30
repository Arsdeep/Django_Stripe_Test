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


def create_checkout_session(request):
    if request.method == 'POST':
        # Get products and quantities from POST
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
        import json
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100),
            currency='usd',
            metadata={
                'cart': json.dumps(cart_items),
            },
        )

        return render(request, 'shop/checkout.html', {
            'client_secret': intent['client_secret'],
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'payment_intent_id': intent['id'],
        })
    return redirect('shop_home')

def confirm_order_payment(request):
    if request.method == 'POST':
        payment_intent_id = request.POST.get('payment_intent_id')
        if not payment_intent_id:
            return JsonResponse({'status': 'failed', 'reason': 'missing_payment_intent'})

        # Retrieve the PaymentIntent from Stripe to verify status
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if intent.status == 'succeeded':
            # Only now create and persist the Order and OrderItems
            import json
            cart_json = intent.metadata.get('cart') if getattr(intent, 'metadata', None) else None
            try:
                cart_items = json.loads(cart_json) if cart_json else []
            except Exception:
                cart_items = []

            if not cart_items:
                return JsonResponse({'status': 'failed', 'reason': 'empty_cart'})

            order = Order.objects.create(paid=True, stripe_payment_intent=payment_intent_id)
            for item in cart_items:
                pid = item.get('product_id')
                qty = int(item.get('quantity', 0))
                if not pid or qty <= 0:
                    continue
                product = Product.objects.get(id=pid)
                OrderItem.objects.create(order=order, product=product, quantity=qty)

            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})