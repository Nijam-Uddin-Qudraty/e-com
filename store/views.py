from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category

def StoreView(req,category_slug=None):
    category = None
    products = None
    product_count = 0
    if category_slug != None:
        category = get_object_or_404(Category,slug = category_slug)
        products = Product.objects.filter(category = category)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context= {
        'products':products,
        'product_count': product_count
    }
    return render(req, 'store/store.html',context)