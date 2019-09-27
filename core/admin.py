from django.contrib import admin

from .models import Articulo, PedidoArticulo, Pedido


admin.site.register(Articulo)
admin.site.register(PedidoArticulo)
admin.site.register(Pedido)
