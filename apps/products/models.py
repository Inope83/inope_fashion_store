from django.db import models


class Kategoria(models.Model):
    naran = models.CharField('Naran', max_length=255)
    deskrisaun = models.TextField('Deskrisaun', blank=True, null=True)

    def __str__(self):
        return self.naran

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategoria sira'


class Produtu(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'),
        ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'),
    ]
    naran = models.CharField('Naran', max_length=255)
    deskrisaun = models.TextField('Deskrisaun', blank=True, null=True)
    presu = models.DecimalField('Presu', max_digits=10, decimal_places=2)
    estok = models.IntegerField('Estok', default=0)
    tamanho = models.CharField('Tamanho', max_length=5, choices=SIZE_CHOICES, blank=True)
    kategoria = models.ForeignKey(
        Kategoria,
        on_delete=models.CASCADE,
        related_name='produtus',
        verbose_name='Kategoria',
    )
    admin = models.ForeignKey(
        'users.Admin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtus',
        verbose_name='Administrador',
    )

    def check_stock(self):
        return self.estok > 0

    def get_featured_image(self):
        feature_image = self.images.filter(is_feature=True).first()
        if feature_image:
            return feature_image
        return self.images.first()

    def __str__(self):
        return self.naran

    class Meta:
        verbose_name = 'Produtu'
        verbose_name_plural = 'Produtu sira'


class ProdutuImage(models.Model):
    produtu = models.ForeignKey(
        Produtu,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Produtu',
    )
    image = models.ImageField('Imajen', upload_to='products/gallery/')
    is_feature = models.BooleanField(
        'Imajen prinsipál',
        default=False,
        help_text='Marka hanesan imajen prinsipál ba produtu ida-ne\'e.',
    )

    def __str__(self):
        return f"Imajen ba {self.produtu.naran}"

    class Meta:
        verbose_name = 'Imajen Produtu'
        verbose_name_plural = 'Imajen Produtu sira'
