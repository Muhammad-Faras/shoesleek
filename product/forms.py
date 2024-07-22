# forms.py
from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full border border-gray-300  p-2 mb-4',  # Add your custom CSS class here
        })
            )
    product_id = forms.IntegerField(widget=forms.HiddenInput)


