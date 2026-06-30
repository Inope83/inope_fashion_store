from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


class Customer(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Kliente'),
        ('admin', 'Administrador'),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
        verbose_name='Uzuáriu',
    )
    phone = models.CharField('Telefone', max_length=20, blank=True)
    role = models.CharField('Papel', max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Kliente (Sistema)'
        verbose_name_plural = 'Kliente Sistema sira'


class Admin(models.Model):
    username = models.CharField('Naran uzuáriu', max_length=150, unique=True)
    password = models.CharField('Liafuan-pase', max_length=255)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administrador sira'


class Kliente(models.Model):
    naran = models.CharField('Naran', max_length=255)
    email = models.EmailField('Email', unique=True)
    password = models.CharField('Liafuan-pase', max_length=255)
    last_login = models.DateTimeField('Tama ikus', null=True, blank=True)
    is_staff = models.BooleanField('Staff', default=False)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.naran

    class Meta:
        verbose_name = 'Kliente'
        verbose_name_plural = 'Kliente sira'


class Notifikasaun(models.Model):
    mensajen = models.TextField('Mensajen')
    tipu = models.CharField('Tipu', max_length=50)
    created_at = models.DateTimeField('Data kria', auto_now_add=True)
    kliente = models.ForeignKey(
        Kliente,
        on_delete=models.CASCADE,
        related_name='notifikasauns',
        verbose_name='Kliente',
    )
    pedidu = models.ForeignKey(
        'orders.Pedidu',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifikasauns',
        verbose_name='Pedidu',
    )

    def __str__(self):
        return f"Notifikasaun ba {self.kliente.naran} - {self.tipu}"

    class Meta:
        verbose_name = 'Notifikasaun'
        verbose_name_plural = 'Notifikasaun sira'
