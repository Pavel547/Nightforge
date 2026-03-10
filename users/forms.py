from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=250, required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'EMAIL',
               'class': 'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'FIRST NAME',
               'class': 'px-1 border-1 borber-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'LAST NAME',
               'class': 'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    password1 = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'PASSWORD1',
               'class': 'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    password2 = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'PASSWORD2',
               'class': 'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        

    def clean_email(self):
        data = self.cleaned_data.get('email')
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('User with this email is already exists')
        return data
        
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = None
        if commit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(required=True, max_length=250, widget=forms.EmailInput(
        attrs={'placeholder': 'EMAIL', 
               'class': 'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    password = forms.CharField(required=True, max_length=250, widget=forms.PasswordInput(
        attrs={'placeholder': 'PASSWORD', 
               'class': 'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))

    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        self.user_cache = authenticate(self.request, username=email, password=password)
        
        if self.user_cache is None:
            raise forms.ValidationError('Invalid password or email')
        elif not self.user_cache.is_active:
            raise forms.ValidationError('User is inactive')
        return self.cleaned_data
    
    
class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=250, required=False, widget=forms.EmailInput(
        attrs={'placeholder':'EMAIL', 
               'class':'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'placeholder':'FIRST NAME',
               'class':'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'placeholder':'LAST NAME',
               'class':'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'placeholder':'COUNTRY',
               'class':'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'placeholder':'CITY',
               'class':'px-1 border-1 border-gray-900 text-lg focus:outine-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'placeholder':'ADDRESS',
               'class':'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    postal_code = forms.CharField(max_length=20, required=True, widget=forms.TextInput(
        attrs={'placeholder':'POSTAL CODE',
               'class':'px-1 border-1 border-gray-900 text-lg focus:outline-none focus:ring-1 focus:ring-gray-400 focus:border-gray-400'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'country', 'city', 'address', 'postal_code']
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('User with this email is already exists')
        return email
    
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email
        
        for field in ['country', 'city', 'postal_code', 'address']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data
