from django.shortcuts import render , get_object_or_404
from django.views.generic import ListView , DetailView
# Create your views here.
from .models import Item , OrderItem , Order
from django.shortcuts import redirect
from django.utils import timezone
# def item_list(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request,"home-page.html",context)

def checkout(request):
    context = {
        'items':Item.objects.all(),
        'orderItem': OrderItem.objects.all(),
        'order': Order.objects.all(),
    }
    return render(request , "checkout.html",context)


def products(request):
    context = {'items':Item,
                'order':Order,
                'orderItem':OrderItem}
    
    return render(request , 'product.html',context)


class HomeView(ListView):
    model = Item

    context_object_name = 'items'
    template_name = "home-page.html"

class ItemDetailView(DetailView):
    model =Item
    template_name = "product.html"

def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item,created = OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date= timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('core:products',slug=slug)



