from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Admins"


class Kliente(models.Model):
    naran = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.naran

    class Meta:
        verbose_name_plural = "Klientes"


class Notifikasaun(models.Model):
    mensajen = models.TextField()
    tipu = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    kliente = models.ForeignKey(
        Kliente,
        on_delete=models.CASCADE,
        related_name='notifikasauns'
    )
    pedidu = models.ForeignKey(
        'orders.Pedidu',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifikasauns'
    )

    def __str__(self):
        return f"Notification for {self.kliente.naran} - {self.tipu}"

    class Meta:
        verbose_name_plural = "Notifikasauns"
