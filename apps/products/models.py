from django.db import models


class Kategoria(models.Model):
    naran = models.CharField(max_length=255)
    deskrisaun = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.naran

    class Meta:
        verbose_name_plural = "Kategorias"


class Produtu(models.Model):
    naran = models.CharField(max_length=255)
    deskrisaun = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='products/', blank=True, null=True)
    kategoria = models.ForeignKey(
        Kategoria,
        on_delete=models.CASCADE,
        related_name='produtus'
    )
    admin = models.ForeignKey(
        'users.Admin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtus'
    )

    def check_stock(self):
        return self.stok > 0

    def get_featured_image(self):
        # Returns the image marked as feature, or the first one, or None
        feature_image = self.images.filter(is_feature=True).first()
        if feature_image:
            return feature_image
        return self.images.first()

    def __str__(self):
        return self.naran

    class Meta:
        verbose_name_plural = "Produtus"


class ProdutuImage(models.Model):
    produtu = models.ForeignKey(
        Produtu,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/gallery/')
    is_feature = models.BooleanField(
        default=False,
        help_text="Set as main thumbnail for the product"
    )

    def __str__(self):
        return f"Image for {self.produtu.name}"
