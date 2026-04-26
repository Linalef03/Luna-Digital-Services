from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'slug', 'description', 'price_from', 'sample_image', 'active']
