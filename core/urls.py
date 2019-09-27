from django.urls import path
from .views import (
    ArticuloDetailView,
    CheckoutView,
    InicioView,
    ResumenPedidoView,
    agregar_al_carrito,
    eliminar_del_carrito,
    eliminar_uno_del_carrito,
    PagoView

)

app_name = 'core'

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('resumen-pedido/', ResumenPedidoView.as_view(), name='resumen-pedido'),
    path('producto/<slug>/', ArticuloDetailView.as_view(), name='producto'),
    path('agregar-al-carrito/<slug>/', agregar_al_carrito, name='agregar-al-carrito'),
    path('eliminar-del-carrito/<slug>/', eliminar_del_carrito, name='eliminar-del-carrito'),
    path('eliminar-articulo-del-carrito/<slug>/', eliminar_uno_del_carrito,
     name='eliminar-uno-del-carrito'),
     path('payment/<opcion_pago>', PagoView.as_view(), name='payment' )
     
]