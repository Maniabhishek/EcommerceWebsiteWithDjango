
from django.urls import path ,include
from .views import (
    HomeView , 
    checkout ,
    add_to_cart,
   )
from .views import ItemDetailView
app_name='core'
urlpatterns = [
    path('',HomeView.as_view(),name='home-page'),
    path('checkout/',checkout,name='checkout'),
    path('products/<slug>/',ItemDetailView.as_view(),name='products'),
    path('add-to-cart/<slug>',add_to_cart,name='add-to-cart'),
   
]