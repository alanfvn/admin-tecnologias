from django.db.models import Sum,F
from django.db.models.functions import ExtractMonth
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import datetime

from dashboard.models import Categoria, DetalleVenta, Producto, Region, Venta

# Create your views here.
class Dashboard(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('authenticate:login')
    template_name = 'inicio.html'
    context_object_name = 'ventas'
    model = Venta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # general data
        context['cat_count'] = Categoria.objects.count() 
        context['prod_count'] = Producto.objects.count()
        context['sell_no'] = Venta.objects.filter(sell_state=False).count()
        context['sell_yes'] = Venta.objects.filter(sell_state=True).count()
        context['regions'] = Region.objects.count()

        curr_year = timezone.now().year

        # query
        result = (
            DetalleVenta.objects
            .filter(sell__sell_date__year=curr_year)
            .annotate(month=ExtractMonth('sell__sell_date'))
            .values('month').annotate(total=Sum(F('qty') * F('price')))
            .order_by('month')
        )
        
        values = [int(res.get('total')) for res in result]

        # current month sales
        context['m_totals'] = values[datetime.now().month-1]
        # total $ per year
        context['y_totals'] = sum(values)
        # total $ per month
        context['sells_month'] = values
 
        return context
