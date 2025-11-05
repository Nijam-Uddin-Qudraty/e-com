from django.shortcuts import render,redirect
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
# Create your views here.
def remove_cart(req, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(req))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1: 
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
def remove_cart_item(req, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(req))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(req, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(req))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except Cart.DoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': round(tax, 2),
        'grand_total': round(grand_total, 2),
    }

    return render(req, 'store/cart.html', context)

def _cart_id(req):
    cart = req.session.session_key
    if not cart:
        cart = req.session.create()
    return cart

def add_cart(req, product_id):
    product = Product.objects.get(id = product_id)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(req))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(req))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()

    return redirect('cart')