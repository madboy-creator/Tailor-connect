from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Producer, Customer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'prod_date', 'image', 'rarity', 'producer']
        widgets = {
            'prod_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = ['name', 'contact_info', 'email', 'location', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_info = forms.CharField(max_length=200, required=True)
    location = forms.CharField(max_length=200, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'contact_info', 'location']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                contact_info=self.cleaned_data['contact_info'],
                location=self.cleaned_data['location']
            )
        return user

class CustomerUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Customer
        fields = ['contact_info', 'location']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        customer = super().save(commit=False)
        if commit:
            customer.user.email = self.cleaned_data['email']
            customer.user.save()
            customer.save()
        return customer