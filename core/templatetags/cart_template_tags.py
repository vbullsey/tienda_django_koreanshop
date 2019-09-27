from django import template
from core.models import Pedido

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Pedido.objects.filter(user=user, fuepedido=False)
        if qs.exists():
            return qs[0].articulos.count()
        return 0