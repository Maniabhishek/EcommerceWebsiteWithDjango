from django import forms
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
