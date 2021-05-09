from django import forms
from django.contrib import messages
from django_countries.fields import CountryField
PAYMENT_CHOICES = (
    ('S', 'stripe'),
    ('p', 'paypal')
)


class CheckoutForm(forms.Form):
    streetAddress = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '20th cross'
    }))
    apartmentAddress = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'apartment or suite'
    }))
    country = CountryField(blank_label='(select country)').formfield(attrs={
        'class': 'custom-select d-block w-100'
    })
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    paymentOption = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': "basic-addon2"
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'row': 3
    }))
    email = forms.EmailField()
