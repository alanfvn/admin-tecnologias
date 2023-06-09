from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum,F,Count
from django.db.models.functions import ExtractMonth
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView

from dashboard.models import Categoria, DetalleVenta, Producto, Region, Venta

class Reports(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('authenticate:login')
    template_name = 'reports.html'
    context_object_name = 'ventas'
    model = Venta


# Create your views here.
class Dashboard(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('authenticate:login')
    template_name = 'inicio.html'
    context_object_name = 'ventas'
    model = Venta

    def sales_per_category(self):
        curr_year = datetime.now().year
        sales_by_category = (
            DetalleVenta.objects
            .filter(sell__sell_date__year=curr_year)
            .values('product__category__name')
            .annotate(total_sales=Sum('qty'))
        )
        total_sales = sum(sale['total_sales'] for sale in sales_by_category)
        sales_percentages = []

        for sale in sales_by_category:
            percentage = (sale['total_sales'] / total_sales) * 100
            sales_percentages.append({
                'name': sale['product__category__name'],
                'y': round(percentage, 4)
            })

        return sales_percentages

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

        # query 2
        sales_details = DetalleVenta.objects.filter(sell__sell_date__year=curr_year)
        sales_by_region = sales_details.values('sell__region__name').annotate(total_sales=Sum(F('qty') * F('price'))).order_by('-total_sales')[:10]

        # query 3
        ventas_del_ano_actual = Venta.objects.filter(sell_date__year=curr_year)
        productos_mas_vendidos = (
            Producto.objects.filter(detalleventa__sell__in=ventas_del_ano_actual) 
            .annotate(total_vendido=Sum('detalleventa__qty')) 
            .annotate(total_venta=F('total_vendido') * F('price')) 
            .order_by('-total_vendido')[:10]
        )

        # query 4
        estados = Venta.objects.values('sell_state').annotate(count=Count('sell_state'))
        states = {str(estado['sell_state']): estado['count'] for estado in estados}

        # query 5
        sells_cat = self.sales_per_category()

        # general data
        context['cat_count'] = Categoria.objects.count() 
        context['prod_count'] = Producto.objects.count()
        context['regions'] = Region.objects.count()
        context['sell_states'] = states
        # sells per region
        context['sells_reg'] = sales_by_region
        # most sold product
        context['prod_sells'] = productos_mas_vendidos
        # current month sales
        context['m_totals'] = values[datetime.now().month-1]
        # total $ per year
        context['y_totals'] = sum(values)
        # total $ per month
        context['sells_month'] = values
        # sells per cat
        context['sells_cat'] = sells_cat

        return context
