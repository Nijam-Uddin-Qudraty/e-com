from django.shortcuts import render
from .models import Product

def StoreView(req):
    products = Product.objects.all().filter(is_available=True)
    product_count = products.count()
    context= {
        'products':products,
        'product_count': product_count
    }
    return render(req, 'store/store.html',context)