from django.db import models

class Kliente(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) # In a real app, use Django's User model

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Klientes"


class Notifikasaun(models.Model):
    message = models.TextField()
    type = models.CharField(max_length=50)
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
        return f"Notification for {self.kliente.name} - {self.type}"

    class Meta:
        verbose_name_plural = "Notifikasauns"
