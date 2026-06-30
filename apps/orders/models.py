from django.db import models


class Pedidu(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Hein prosesu'),
        ('konfirmadu', 'Konfirmadu ona'),
        ('envia', 'Haruka ona'),
        ('entrega', 'Simu ona'),
        ('kansela', 'Kansela ona'),
    ]
    status = models.CharField('Estadu', max_length=50, choices=STATUS_CHOICES, default='pendente')
    total = models.DecimalField('Totál', max_digits=10, decimal_places=2)
    enderesu = models.TextField('Enderesu', default='')
    created_at = models.DateTimeField('Data kria', auto_now_add=True)
    kliente = models.ForeignKey(
        'users.Kliente',
        on_delete=models.CASCADE,
        related_name='pedidus',
        verbose_name='Kliente',
    )
    admin = models.ForeignKey(
        'users.Admin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidus',
        verbose_name='Administrador',
    )

    def __str__(self):
        return f"Pedidu {self.id} - {self.kliente.naran}"

    class Meta:
        verbose_name = 'Pedidu'
        verbose_name_plural = 'Pedidu sira'


class DetalloPedidu(models.Model):
    kantidade = models.IntegerField('Kantidade')
    subtotal = models.DecimalField('Subtotál', max_digits=10, decimal_places=2)
    pedidu = models.ForeignKey(
        Pedidu,
        on_delete=models.CASCADE,
        related_name='detallos',
        verbose_name='Pedidu',
    )
    produtu = models.ForeignKey(
        'products.Produtu',
        on_delete=models.CASCADE,
        related_name='pedidu_detallos',
        verbose_name='Produtu',
    )

    def __str__(self):
        return f"{self.kantidade}x {self.produtu.naran} (Pedidu {self.pedidu.id})"

    class Meta:
        verbose_name = 'Detallu Pedidu'
        verbose_name_plural = 'Detallu Pedidu sira'


class Pagamentu(models.Model):
    METHOD_CHOICES = [
        ('cod', 'COD (Selu bainhira simu)'),
        ('transfer', 'Transferénsia bankária'),
        ('mbway', 'MBWAY'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Hein selu'),
        ('pagu', 'Selu ona'),
        ('kansela', 'Kansela ona'),
    ]
    metodu = models.CharField('Metodu', max_length=50, choices=METHOD_CHOICES)
    total = models.DecimalField('Totál', max_digits=10, decimal_places=2)
    status = models.CharField('Estadu', max_length=50, choices=STATUS_CHOICES, default='pendente')
    created_at = models.DateTimeField('Data kria', auto_now_add=True)
    pedidu = models.OneToOneField(
        Pedidu,
        on_delete=models.CASCADE,
        related_name='pagamentu',
        verbose_name='Pedidu',
    )
    admin = models.ForeignKey(
        'users.Admin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagamentus',
        verbose_name='Administrador',
    )

    def __str__(self):
        return f"Pagamentu ba Pedidu {self.pedidu.id} - {self.get_status_display()}"

    class Meta:
        verbose_name = 'Pagamentu'
        verbose_name_plural = 'Pagamentu sira'
