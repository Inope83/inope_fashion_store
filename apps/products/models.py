from django.db import models

class Kategoria(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Kategorias"


class Produtu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    kategoria = models.ForeignKey(
        Kategoria,
        on_delete=models.CASCADE,
        related_name='produtus'
    )

    def check_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Produtus"
