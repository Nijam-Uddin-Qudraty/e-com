
from django.urls import path
from . import views

urlpatterns = [
    path("",views.StoreView,name='store'),
    path("<slug:category_slug>/",views.StoreView,name='products_by_category'),
    path("<slug:category_slug>/<slug:product_slug>/",views.product_details,name='product_detail'),
] 