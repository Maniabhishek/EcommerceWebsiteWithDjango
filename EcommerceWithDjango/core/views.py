import string
import random
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import Coupon, Item, OrderItem, Order, BillingAddress, Payment, Refund
from django.shortcuts import redirect
from django.utils import timezone
from . forms import CheckoutForm, CouponForm, RefundForm
from django.http import HttpResponseRedirect, request
import stripe
from django.conf import settings
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


def create_ref():
    return "".join(random.choices(string.ascii_lowercase + string.digits + string.digits, k=20))

# def item_list(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request,"home-page.html",context)


def CheckoutView(request):
    if request.method == 'POST':
        print("post method")
        print(request.POST)
        form = CheckoutForm(request.POST)
        try:
            order = Order.objects.get(user=request.user, ordered=False)

            if form.is_valid():
                print("form is valid ====== ")
                streetAddress = form.cleaned_data.get('streetAddress')
                apartmentAddress = form.cleaned_data.get('apartmentAddress')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO : add functionality for these fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                paymentOption = form.cleaned_data.get('paymentOption')
                print("payment option is==========", paymentOption)
                print(request.user)
                billling_address = BillingAddress(
                    user=request.user,
                    streetAddress=streetAddress,
                    apartmentAddress=apartmentAddress,
                    countries=country,
                    zip=zip,
                    address_type='B'

                )
                billling_address.save()

                print(f'here is the billing addres {billling_address}')

                order.billingAddress = BillingAddress(
                    user=request.user,
                    streetAddress=streetAddress,
                    apartmentAddress=apartmentAddress,
                    countries=country,
                    zip=zip,

                )
                order.save()
                # TODO: add redirect to the selected payment option
                print("form is valid")
                if paymentOption == 'S':
                    return redirect('core:payment')
                elif paymentOption == 'P':
                    return redirect('core:payment')
                else:
                    messages.warning(
                        request, "Invalid payment option selected")
                    return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.error(request, "You do not have an active order")
            return redirect("core:payment")
        # print(request.POST)

    else:

        order = Order.objects.get(user=request.user, ordered=False)
        form = CheckoutForm()

        context = {
            'form': form,
            'order': order,
            'couponform': CouponForm(),
            'DISPLAY_COUPON_FORM': True

        }
        return render(request, "checkout.html", context)

# class CheckoutView(View):


#     def get(self,*args , **kwargs):
#         form = CheckoutForm()
#         print("abhishek")
#         print(self.request.get_full_path)
#         context = {
#             'form':form
#         }

#         return render(self.request , "checkout.html",context)
#     def post(self , *args , **kwargs):
#         print("post ,method")
#         form = CheckoutForm(self.request.POST)
#         print(self.request.POST)
#         if form.is_valid():
#             # print(f'cleaned data = {form.cleaned_data}')
#             print("form is valid")
#             # messages.warning(self.request,"Failed Checkout")

#             return redirect('core:checkout')
#         print("post method final return")
#         messages.warning(self.request,"Failed Checkout")
#         return redirect('core:checkout')

def PaymentView(request):
    # def get(self, *args ,**kwargs):
    #     return render(self.request, 'payment.html')

    if request.method == 'POST':
        order = Order.objects.get(user=request.user, ordered=False)

        token = request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        print("totalm amountis here ======", amount)
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token,
                description="My First Test Charge (created for API docs)",
            )

        # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = request.user
            payment.amount = order.get_total()
            print(order.get_total())
            payment.save()
            # assign the payment to the order
            order_item = order.items.all()
            order_item.update(ordered=True)
            for item in order_item:
                item.save()
            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref()
            order.save()
            messages.success(request, "your order was successfull")
            return redirect("/")
            # Use Stripe's library to make requests...

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"{err.get('message')}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "Rate Limit Error")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid Parameters")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Not authenticated")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "Network Error")
            return redirect("/")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(
                request, "Something went wrong , you are not charged , please try again")
            return redirect("/")
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(
                request, "A serious error occured . We have been notified")
            return redirect("/")

    else:
        order = Order.objects.get(user=request.user, ordered=False)
        if order.billling_address or True:  # True condition is not required
            context = {
                'order': order,
                'couponform': CouponForm(),
                'DISPLAY_COUPON_FORM': False

            }
            return render(request, 'payment.html', context)
        else:
            messages.warning(request, "You do not have added billing address")
            return redirect("core:checkout")
        # `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            print("in order summary ")
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object': order}
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


def products(request):
    context = {'items': Item,
               'order': Order,
               'orderItem': OrderItem}

    return render(request, 'product.html', context)


class HomeView(ListView):
    model = Item
    paginate_by = 10
    context_object_name = 'items'
    template_name = "home-page.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    print("add to cart running?")
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("core:orderSummary")

        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect("core:orderSummary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect('core:orderSummary')

    return redirect('core:orderSummary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)

            messages.info(request, "This item was removed from your cart")
            return redirect('core:orderSummary')

        else:
            # add a message saying the order does not contain any order
            messages.info(request, "This item was not in your cart")

            return redirect('core:products', slug=slug)
    else:
        # add a message saying the order does not contain any order
        messages.info(request, "you do not have an active order")

        return redirect('core:products', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity updated")

        else:
            # add a message saying the order does not contain any order
            messages.info(request, "This item was not in your cart")

            return redirect('core:orderSummary')
    else:
        # add a message saying the order does not contain any order
        messages.info(request, "you do not have an active order")

        return redirect('core:orderSummary')
    return redirect('core:orderSummary')


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


def add_coupon(request):
    if request.method == "POST":
        print(request.POST['code'])
        form = CouponForm(request.POST)
        if form.is_valid():

            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=request.user, ordered=False)
                coupon = get_coupon(request, code)
                order.coupon = coupon
                order.save()
                messages.info(request, "Successfully applied coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(request, "You do not have the active orders")
        else:
            messages.info(request, "This coupon does not exist")
            return redirect("core:checkout")
    return None


class RequestRefund(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {'form': form}
        return render(self.request, 'refund-request.html', context)

    def post(self, *args, **kwargs):
        refundForm = RefundForm(self.request.POST)
        if refundForm.is_valid():
            ref_code = refundForm.cleaned_data.get('ref_code')
            message = refundForm.cleaned_data.get('message')
            email = refundForm.cleaned_data.get('email')
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.warning(self.request, "request recieved")
                return redirect("core:request-refund")
            except ObjectDoesNotExist:
                messages.warning(self.request, "You do not have the order ")
                return redirect("core:request-refund")
