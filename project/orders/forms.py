from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["service", "description", "budget"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

# Form final files
class CompleteOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["final_file"]
