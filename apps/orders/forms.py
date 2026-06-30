from django import forms
from .models import Pedidu


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Pedidu
        fields = ['enderesu']
        labels = {
            'enderesu': 'Enderesu entrega',
        }
        widgets = {
            'enderesu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Rua, númeru, suku, munisípiu...',
            }),
        }
