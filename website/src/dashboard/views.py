from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from dashboard.models import Categoria, Producto, Venta

# Create your views here.
class Dashboard(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('authenticate:login')
    template_name = 'inicio.html'
    context_object_name = 'ventas'
    model = Venta


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cat_count'] = Categoria.objects.count() 
        context['prod_count'] = Producto.objects.count()
        context['sell_no'] = Venta.objects.filter(sell_state=False).count()
        context['sell_yes'] = Venta.objects.filter(sell_state=True).count()

        return context
