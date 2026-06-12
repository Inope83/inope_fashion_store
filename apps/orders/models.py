from django.db import models

class Pedidu(models.Model):
    status = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    kliente = models.ForeignKey(
        'users.Kliente',
        on_delete=models.CASCADE,
        related_name='pedidus'
    )

    def __str__(self):
        return f"Order {self.id} - {self.kliente.name}"

    class Meta:
        verbose_name_plural = "Pedidus"


class DetalloPedidu(models.Model):
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    pedidu = models.ForeignKey(
        Pedidu,
        on_delete=models.CASCADE,
        related_name='detallos'
    )
    produtu = models.ForeignKey(
        'products.Produtu',
        on_delete=models.CASCADE,
        related_name='pedidu_detallos'
    )

    def __str__(self):
        return f"{self.quantity}x {self.produtu.name} (Order {self.pedidu.id})"

    class Meta:
        verbose_name_plural = "Detallo Pedidus"


class Pagamentu(models.Model):
    method = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    pedidu = models.OneToOneField(
        Pedidu,
        on_delete=models.CASCADE,
        related_name='pagamentu'
    )

    def __str__(self):
        return f"Payment for Order {self.pedidu.id} - {self.status}"

    class Meta:
        verbose_name_plural = "Pagamentus"
