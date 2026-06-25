from django import forms


class AddToCartForm(forms.Form):
    produtu_id = forms.IntegerField(widget=forms.HiddenInput)
    kantidade = forms.IntegerField(min_value=1, initial=1, label='Kantidade')
