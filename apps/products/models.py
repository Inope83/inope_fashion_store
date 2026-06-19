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

    def check_stock(self):
        return self.stok > 0

    def __str__(self):
        return self.naran

    class Meta:
        verbose_name_plural = "Produtus"
