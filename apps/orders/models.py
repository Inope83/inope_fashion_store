from django.db import models


class Pedidu(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('konfirmadu', 'Konfirmadu'),
        ('envia', 'Envia'),
        ('entrega', 'Entrega'),
        ('kansela', 'Kansela'),
    ]
    estado = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    endeereco_entrega = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    kliente = models.ForeignKey(
        'users.Kliente',
        on_delete=models.CASCADE,
        related_name='pedidus'
    )
    admin = models.ForeignKey(
        'users.Admin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidus'
    )

    def __str__(self):
        return f"Order {self.id} - {self.kliente.naran}"

    class Meta:
        verbose_name_plural = "Pedidus"


class DetalloPedidu(models.Model):
    kantidade = models.IntegerField()
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
        return f"{self.kantidade}x {self.produtu.naran} (Order {self.pedidu.id})"

    class Meta:
        verbose_name_plural = "Detallo Pedidus"


class Pagamentu(models.Model):
    METHOD_CHOICES = [
        ('cod', 'COD (Selu Bainhira Simu)'),
        ('transfer', 'Transferensia Bankaria'),
        ('mbway', 'MBWAY'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pagu', 'Pagu'),
        ('kansela', 'Kansela'),
    ]
    metodu = models.CharField(max_length=50, choices=METHOD_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pendente')
    created_at = models.DateTimeField(auto_now_add=True)
    pedidu = models.OneToOneField(
        Pedidu,
        on_delete=models.CASCADE,
        related_name='pagamentu'
    )
    admin = models.ForeignKey(
        'users.Admin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagamentus'
    )

    def __str__(self):
        return f"Payment for Order {self.pedidu.id} - {self.estado}"

    class Meta:
        verbose_name_plural = "Pagamentus"
