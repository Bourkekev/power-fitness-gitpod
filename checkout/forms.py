from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Creates the Checkout form.
    It will not include automatically generated fields.
    """
    class Meta:
        # which model and which fields
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # auto focus on name field
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # add star on required fields
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            # set placeholder values
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # add stripe class
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
