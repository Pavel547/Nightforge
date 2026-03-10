from django import forms
from django.utils.html import strip_tags

class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='FIRST_NAME', widget=forms.TextInput(
        attrs={
            'placeholder': 'FIRST NAME',
            'class': 'px-1 border-1 border-gray-900 text-xl focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'
        }
    ))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'placeholder': 'LAST NAME', 
            'class': 'px-1 border-1 border-gray-900 text-xl focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'
        }
    ))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={
            'placeholder': 'EMAIL',
            'class': 'px-1 border-1 border-gray-900 text-xl focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'
        }
    ))
    country = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'placeholder': 'COUNTRY',
            'class': 'px-1 border-1 border-gray-900 text-xl focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'
        }
    ))
    city = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'placeholder': 'CITY', 
            'class': 'px-1 border-1 border-gray-900 text-xl focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'
        }
    ))
    address = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'placeholder': 'ADDRESS', 
            'class': 'px-1 border-1 border-gray-900 text-xl focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'
        }
    ))
    postal_code = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={
            'placeholder': 'POSTAL CODE', 
            'class': 'px-1 border-1 border-gray-900 text-xl focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'
        }
    ))
    
# Method for initializing existing user data in forms
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        field_list=[
            'first_name', 'last_name', 'email', 'country',
            'city', 'address', 'postal_code', 
            ]
        
        if user:
            for field in field_list:
                self.fields[field].initial = getattr(user, field)

# Clear form inputs data from html tags    
    def clean(self):
        cleaned_data = super().clean()
        
        field_list = ['country', 'city', 'address', 'postal_code']
        
        for field in field_list:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data
            
        