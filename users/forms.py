from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Review


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


class CreatorForm(forms.ModelForm):
    avatar = forms.FileField()
    banner = forms.FileField()

    bio = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    price = forms.FloatField()

    class Meta:
        model = Profile
        fields = ["avatar", "banner", "bio", "price"]


class ReviewForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "What is your voice request?", "rows": 10}), label="")
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5', 'step': '1', 'hidden': True}))

    class Meta:
        model = Review
        fields = ["body", "rating"]
