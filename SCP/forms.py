from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from User.models import Customer, Store, Workshop
from .models import Parts, Part_Image

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email', 'username', 'password1', 'password2']




class StoreCreationForm(UserCreationForm):
    class Meta:
        model = Store
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})




class WorkshopUserCreationForm(UserCreationForm):
    class Meta:
        model = Workshop 
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['email'].widget.attrs.update({'class': 'form-control'})
           self.fields['username'].widget.attrs.update({'class': 'form-control'})
           self.fields['password1'].widget.attrs.update({'class': 'form-control'})
           self.fields['password2'].widget.attrs.update({'class': 'form-control'})



class AddPartsForm(ModelForm):
    class Meta:
        model = Parts
        fields = '__all__'



class PartsImages(forms.Form):
    image_field = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['image_field'].widget.attrs.update({'class': 'form-control'})
           
class ServiceImage(forms.Form):
    image_field = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['image_field'].widget.attrs.update({'class': 'form-control'})



class AddserviceForm(forms.Form):
    name = forms.CharField()
    price = forms.FloatField()
    des = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['name'].widget.attrs.update({'class': 'form-control'})
           self.fields['price'].widget.attrs.update({'class': 'form-control'})
           self.fields['des'].widget.attrs.update({'class': 'form-control'})




class Dateandtime(forms.Form):
    date = forms.DateField(widget=forms.DateInput())
    time = forms.TimeField(widget=forms.TimeInput())




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())



class UpdateCart(forms.Form):
    Quantity=forms.IntegerField()
 