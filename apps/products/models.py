from django.db import models


class Kategoria(models.Model):
    naran = models.CharField(max_length=255)
    deskrisaun = models.TextField(blank=True)

    @classmethod
    def list_all(cls):
        return cls.objects.all()

    def __str__(self):
        return self.naran

    class Meta:
        verbose_name_plural = "Kategorias"


class Produtu(models.Model):
    naran = models.CharField(max_length=255)
    deskrisaun = models.TextField(blank=True)
    preco = models.FloatField()
    stok = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='produtu/', blank=True, null=True)
    kategoria = models.ForeignKey(
        Kategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtu_set'
    )

    def check_stock(self):
        return self.stok > 0

    def __str__(self):
        return self.naran

    class Meta:
        verbose_name_plural = "Produtus"