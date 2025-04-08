from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Ad,Contact

class RegUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class AdForm(forms.ModelForm):
    
    class Meta:
        model = Ad
        exclude = ['user']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['message']