from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm
from .models import Articulo, PedidoArticulo, Pedido, DireccionEnvio



def productos(request):
    context = {
        'articulos': Articulo.objects.all()
    }
    return render(request, "product.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            pedido = Pedido.objects.get(user=self.request.user, fuepedido=False)
            if form.is_valid():
                direccion = form.cleaned_data.get('direccion')
                direccion_departamento = form.cleaned_data.get('direccion_departamento')
                comuna = form.cleaned_data.get('comuna')
                zip = form.cleaned_data.get('zip')
                # TODO: 
                #misma_direccion_pago = form.cleaned_data.get('misma_direccion_pago')
                #guardar_informacion = form.cleaned_data.get('guardar_informacion')
                opcion_pago = form.cleaned_data.get('opcion_pago')
                direccion_envio = DireccionEnvio(
                user=self.request.user,
                direccion=direccion,
                direccion_departamento=direccion_departamento,
                comuna=comuna,
                zip=zip
                )
                direccion_envio.save()
                pedido.direccion_envio = direccion_envio
                pedido.save()
                print(form.cleaned_data) 
                print("El formulario es válido")
                return redirect('core:checkout')
            messages.warning(self.request, "Fallo en el Pago!")
            return redirect('core:checkout')
        
        except ObjectDoesNotExist:
            messages.error(self.request, "No posees un pedido activo")
            return redirect("core:resumen-pedido")

class PagoView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "payment.html")


        
class InicioView(ListView):
    model = Articulo
    paginate_by = 5
    template_name = "home.html"


class ResumenPedidoView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            pedido = Pedido.objects.get(user=self.request.user, fuepedido=False)
            context = {
                'object': pedido
            }
            return render(self.request, 'resumen_pedido.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "No posees un pedido activo")
            return redirect("/")
            
class ArticuloDetailView(DetailView):
    model = Articulo
    template_name = "product.html"

@login_required
def agregar_al_carrito(request, slug):
    articulo = get_object_or_404(Articulo, slug=slug)
    pedido_articulo, created = PedidoArticulo.objects.get_or_create(
        articulo=articulo,
        user=request.user,
        fuepedido=False
    )
    pedido_qs = Pedido.objects.filter(user=request.user, fuepedido=False)
    if pedido_qs.exists():
        pedido = pedido_qs[0]
        #Comprueba si existe un pedido de esta orden
        if pedido.articulos.filter(articulo__slug=articulo.slug).exists():
           pedido_articulo.cantidad +=1
           pedido_articulo.save()
           messages.info(request, "La cantidad de este pedido fue aumentada")
           return redirect("core:resumen-pedido")
        else:
            pedido.articulos.add(pedido_articulo)
            messages.info(request, "Articulo añadido a su carrito")
            return redirect("core:producto", slug=slug)

    else:
        orden_pedido = timezone.now()
        pedido = Pedido.objects.create(
            user=request.user, orden_pedido=orden_pedido)
        pedido.articulos.add(pedido_articulo)
        messages.info(request, "Articulo añadido a su carrito")
    return redirect("core:producto", slug=slug)


@login_required
def eliminar_del_carrito(request, slug):
    articulo = get_object_or_404(Articulo, slug=slug)
    pedido_qs = Pedido.objects.filter(
        user=request.user,
        fuepedido=False
    )
    if pedido_qs.exists():
        pedido = pedido_qs[0]
        #Comprueba si existe un pedido de esta orden
        if pedido.articulos.filter(articulo__slug=articulo.slug).exists():
            pedido_articulo = PedidoArticulo.objects.filter(
                articulo=articulo,
                user=request.user,
                fuepedido=False
            )[0]        
            pedido.articulos.remove(pedido_articulo)
            messages.info(request, "Articulo eliminado de su carrito.")
            return redirect("core:resumen-pedido") 
        else:
             messages.info(request, "No tiene ningun producto en su carrito")
             return redirect("core:producto", slug=slug)           
    else:
        messages.info(request, "No tienes una orden activa")
        return redirect("core:producto", slug=slug)         
    


@login_required
def eliminar_uno_del_carrito(request, slug):
    articulo = get_object_or_404(Articulo, slug=slug)
    pedido_qs = Pedido.objects.filter(
        user=request.user,
        fuepedido=False
    )
    if pedido_qs.exists():
        pedido = pedido_qs[0]
        #Comprueba si existe un pedido de esta orden
        if pedido.articulos.filter(articulo__slug=articulo.slug).exists():
            pedido_articulo = PedidoArticulo.objects.filter(
                articulo=articulo,
                user=request.user,
                fuepedido=False
            )[0]        
            if  pedido_articulo.cantidad > 1:
                pedido_articulo.cantidad -=1
                pedido_articulo.save()

            else:
                pedido.articulos.remove(pedido_articulo)
            messages.info(request, "Cantidad disminuida!")
            return redirect("core:resumen-pedido") 

        else:
            messages.info(request, "No tiene ningun producto en su carrito")
            return redirect("core:producto", slug=slug)
    else:
        messages.info(request, "No tienes ninga orden activa")
        return redirect("core:producto", slug=slug)


    
