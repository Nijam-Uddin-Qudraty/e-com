from django.shortcuts import render,get_object_or_404
from .models import Product
from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from django.shortcuts import render, get_object_or_404
from category.models import Category
from store.models import Product
from cart.models import Cart, CartItem
from cart.views import _cart_id

def StoreView(req, category_slug=None):
    category = None
    products = None
    product_count = 0
    in_cart = []

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        paginator = Paginator(products, 6)
        page = req.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    # Check which products are in the cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(req))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        in_cart = [item.product.id for item in cart_items]
    except Cart.DoesNotExist:
        in_cart = []

    context = {
        'products': paged_products,
        'product_count': product_count,
        'in_cart': in_cart,
    }

    return render(req, 'store/store.html', context)

def product_details(req,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(req), product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    return render(req,'store/product_detail.html',context)