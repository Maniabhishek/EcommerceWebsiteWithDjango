
from django.urls import path ,include
from .views import (
    HomeView , 
    CheckoutView ,
    add_to_cart,
    OrderSummaryView,
    remove_from_cart,
    remove_single_item_from_cart,
   )
from .views import ItemDetailView
app_name='core'
urlpatterns = [
    path('',HomeView.as_view(),name='home-page'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('orderSummary/',OrderSummaryView.as_view(),name='orderSummary'),
    path('products/<slug>/',ItemDetailView.as_view(),name='products'),
    path('add-to-cart/<slug>',add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>',remove_from_cart,name='remove-from-cart'),
    path('remove-single-item/<slug>',remove_single_item_from_cart,name='removing-single-item'),

]