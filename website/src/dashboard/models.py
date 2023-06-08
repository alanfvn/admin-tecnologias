from datetime import datetime
from django.db import models

# modelo de categoria
class Categoria(models.Model):
    name = models.TextField(verbose_name="Nombre", unique=True, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['id']


# modelo de producto
class Producto(models.Model):
    name = models.TextField(verbose_name="Nombre", unique=True, blank=False)
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    price = models.DecimalField(default=0.0, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

    def __str__(self):
        return self.name


# modelo de region
class Region(models.Model):
    name = models.TextField(verbose_name='Nombre', unique='True', blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regiones'
        ordering = ['id']

# modelo de ventas
class Venta(models.Model):
    sell_date = models.DateTimeField(default=datetime.now)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region', blank=False)
    sell_state = models.BooleanField(verbose_name='Estado de venta', blank=False)

# modelo detalle de venta
class DetalleVenta(models.Model):
    sell = models.ForeignKey(Venta, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(default=0.0, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
