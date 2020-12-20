from django.shortcuts import render , get_object_or_404
from django.views.generic import ListView , DetailView ,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
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


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args , **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered = False)
            context = {'object':order}
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("/")
    

def products(request):
    context = {'items':Item,
                'order':Order,
                'orderItem':OrderItem}
    
    return render(request , 'product.html',context)


class HomeView(ListView):
    model = Item
    paginate_by = 10
    context_object_name = 'items'
    template_name = "home-page.html"

class ItemDetailView(DetailView):
    model =Item
    template_name = "product.html"


@login_required
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
            messages.info(request,"This item quantity was updated")
            
        else:
            order.items.add(order_item)
            messages.info(request,"This item was added to your cart")
            return redirect("core:orderSummary")
    else:
        ordered_date= timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This item was added to your cart")
        return redirect('core:orderSummary')

    return redirect('core:orderSummary')


@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item , slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            order.items.remove(order_item)
            
            messages.info(request,"This item was removed from your cart")
            return redirect('core:orderSummary')
            
        else:
            # add a message saying the order does not contain any order
            messages.info(request,"This item was not in your cart")

            return redirect('core:products',slug=slug)
    else:
        # add a message saying the order does not contain any order
        messages.info(request,"you do not have an active order")

        return redirect('core:products',slug=slug)
    

@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item , slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            if order_item.quantity>1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request,"This item quantity updated")
            
        else:
            # add a message saying the order does not contain any order
            messages.info(request,"This item was not in your cart")

            return redirect('core:orderSummary')
    else:
        # add a message saying the order does not contain any order
        messages.info(request,"you do not have an active order")

        return redirect('core:orderSummary')
    return redirect('core:orderSummary')

