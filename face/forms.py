from django import forms
from django.forms import ModelForm
from .models import FaceHist

class FaceForm(forms.ModelForm):
    class Meta:
        model = FaceHist
        fields = ['age', 'gender','image']
        labels = {
            'age':('나이'),
            'gender':('연령'),
            'image':('이미지'),
        }