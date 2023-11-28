from django import forms
from .models import VocalRequest

class RequestForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "What is your voice request?", "rows": 10}), label="")

    class Meta:
        model = VocalRequest
        fields = ["body"]
