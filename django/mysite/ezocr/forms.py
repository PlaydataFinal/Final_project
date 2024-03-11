from django import forms
from .models import EzocrResult

class EzocrForm(forms.ModelForm):
    class Meta:
        model = EzocrResult
        fields = ['image']