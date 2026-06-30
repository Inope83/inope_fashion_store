from django import forms
from django.contrib.auth.hashers import make_password
from apps.users.models import Kliente, Admin
from apps.products.models import Produtu, ProdutuImage


def validate_password_strength(password):
    if not password:
        return
    if len(password) < 8:
        raise forms.ValidationError('Liafuan-pase tenke minimu karakter 8.')
    if not any(char.isdigit() for char in password):
        raise forms.ValidationError('Liafuan-pase tenke iha numeru ida (0-9).')


class DashboardKlienteForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False, attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True,
        help_text='Liafuan-pase foun (minimu 8 karakter, no numeru ida). Wainhira edita, husik mamuk atu la troka.'
    )

    class Meta:
        model = Kliente
        fields = ['naran', 'email', 'password']
        widgets = {
            'naran': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naran kliente'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email kliente'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password'].initial = ''

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password_strength(password)
        return password

    def save(self, commit=True):
        kliente = super().save(commit=False)
        new_password = self.cleaned_data.get('password')
        if self.instance and self.instance.pk and not new_password:
            # Restore original hashed password
            original = Kliente.objects.get(pk=self.instance.pk)
            kliente.password = original.password
        elif new_password:
            kliente.password = new_password  # Will be hashed on model save()
        if commit:
            kliente.save()
        return kliente


class DashboardAdminForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False, attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True,
        help_text='Liafuan-pase foun (minimu 8 karakter, no numeru ida). Wainhira edita, husik mamuk atu la troka.'
    )

    class Meta:
        model = Admin
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naran administrador'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password'].initial = ''

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password_strength(password)
        return password

    def save(self, commit=True):
        admin = super().save(commit=False)
        new_password = self.cleaned_data.get('password')
        if self.instance and self.instance.pk and not new_password:
            # Restore original hashed password
            original = Admin.objects.get(pk=self.instance.pk)
            admin.password = original.password
        elif new_password:
            admin.password = new_password  # Will be hashed on model save()
        if commit:
            admin.save()
        return admin


class DashboardProdutuForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        help_text='PNG, JPG, JPEG. Tama 1MB.',
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 1 * 1024 * 1024:
            raise forms.ValidationError('Imajen boot liu. Tama máximu 1MB.')
        return image
    image_clear = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Hamos imajen',
    )

    class Meta:
        model = Produtu
        fields = ['naran', 'deskrisaun', 'presu', 'estok', 'tamanho', 'kategoria']
        widgets = {
            'naran': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naran produtu'}),
            'deskrisaun': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Deskrisaun produtu', 'rows': 3}),
            'presu': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'estok': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'tamanho': forms.Select(attrs={'class': 'form-control'}),
            'kategoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            featured = self.instance.images.filter(is_feature=True).first()
            if not featured:
                featured = self.instance.images.first()
            if featured:
                self.fields['image'].help_text = f'Aktuál: {featured.image.url}. Troka ka husik mamuk.'
                self.initial['image'] = featured.image

    def save(self, commit=True):
        produtu = super().save(commit=False)
        if commit:
            produtu.save()
        image_file = self.cleaned_data.get('image')
        image_clear = self.cleaned_data.get('image_clear')
        if image_clear:
            produtu.images.all().delete()
        if image_file:
            produtu.images.all().delete()
            ProdutuImage.objects.create(
                produtu=produtu,
                image=image_file,
                is_feature=True,
            )
        return produtu
