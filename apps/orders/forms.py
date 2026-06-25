from django import forms
from .models import Pedidu


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Pedidu
        fields = ['endeereco_entrega']
