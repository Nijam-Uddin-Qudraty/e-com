
from django.urls import path
from . import views

urlpatterns = [
    path("",views.StoreView,name='store'),
    path("<slug:category_slug>/",views.StoreView,name='products_by_category'),
] 