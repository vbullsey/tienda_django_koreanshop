from django.conf import settings
from django.db import models
from django.shortcuts import reverse


ELECCION_CATEGORIA = ( 
    ('PO', 'Polera'),
    ('FA', 'Falda'),
    ('PN', 'Polerones'),
    ('VT', 'Vestidos')
)

ELECCION_ETIQUETA = ( 
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Articulo(models.Model):
    titulo = models.CharField(max_length=100)
    precio = models.IntegerField()
    precio_descuento = models.IntegerField(blank=True, null=True)
    categoria = models.CharField(choices=ELECCION_CATEGORIA, max_length=2)
    etiqueta = models.CharField(choices=ELECCION_ETIQUETA, max_length=1)
    slug = models.SlugField()
    descripcion = models.TextField()
    cantidad = models.IntegerField(default=1)
    image = models.ImageField()

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse("core:producto", kwargs={
           'slug': self.slug
        })

    def get_añadir_al_carrito_url(self):
        return reverse("core:agregar-al-carrito", kwargs={
           'slug': self.slug
        })
    
    def get_eliminar_del_carrito_url(self):
        return reverse("core:eliminar-del-carrito", kwargs={
           'slug': self.slug
        })
        

class PedidoArticulo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    fuepedido = models.BooleanField(default=False)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.cantidad} of {self.articulo.titulo}"
    
    def get_precio_total_articulo(self):
        return self.cantidad * self.articulo.precio

    def get_precio_total_descuento_articulo(self):
        return self.cantidad * self.articulo.precio_descuento

    def get_cantidad_ahorrada(self):
        return self.get_precio_total_articulo() - self.get_precio_total_descuento_articulo()

    def get_precio_final(self):
        if self.articulo.precio_descuento:
            return self.get_precio_total_descuento_articulo()
        return self.get_precio_total_articulo()


class Pedido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    articulos = models.ManyToManyField(PedidoArticulo)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    orden_pedido = models.DateTimeField()
    fuepedido = models.BooleanField(default=False)
    direccion_envio = models.ForeignKey(
        'DireccionEnvio', on_delete=models.SET_NULL, blank=True, null=True)

    
    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for pedido_articulo in self.articulos.all():
            total += pedido_articulo.get_precio_final()
        return total


class DireccionEnvio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    direccion_departamento = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username
        


