from django import forms
from .models import Kliente


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Kliente
        fields = ['naran', 'email']
        labels = {'naran': 'Naran', 'email': 'Email'}


class LoginForm(forms.Form):
    email = forms.CharField(label='Email / Uzuáriu')
    password = forms.CharField(label='Liafuan-pase', widget=forms.PasswordInput)


class RegistForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Liafuan-pase')

    class Meta:
        model = Kliente
        fields = ['naran', 'email', 'password']
        labels = {
            'naran': 'Naran',
            'email': 'Email',
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm = self.data.get('confirm_password')
        if password:
            if len(password) < 8:
                raise forms.ValidationError('Liafuan-pase tenke minimu karakter 8.')
            if not any(char.isdigit() for char in password):
                raise forms.ValidationError('Liafuan-pase tenke iha numeru ida (0-9).')
            if password != confirm:
                raise forms.ValidationError('Liafuan-pase ho konfirmasaun la hanesan.')
        return password
