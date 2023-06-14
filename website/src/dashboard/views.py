from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum,F,Count
from django.db.models.functions import ExtractMonth, TruncDate
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView
from dashboard.forms import ReportForm

from dashboard.models import Categoria, DetalleVenta, Producto, Region, Venta

class Reports(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('authenticate:login')
    success_url = reverse_lazy('dashboard:reports')
    template_name = 'reports.html'
    form_class = ReportForm

    def get_filter_region(self):
        user = self.request.user
        region = user.region
        if user.groups.filter(name="Director general").exists():
            return None
        return region

    def get_initial(self):
        initial = super().get_initial()
        initial['region'] = self.get_filter_region() or 'Todas las regiones'
        return initial

    def sales_by_range(self, start, end):
        reg = self.get_filter_region()
        ventas_dia = (DetalleVenta.objects
            .filter(sell__sell_date__range=(start, end))
            .annotate(day=TruncDate('sell__sell_date'))
            .values('day')
            .annotate(total_ventas=Sum(F('qty') * F('price')))
            .order_by('day')
        )

        if reg:
            ventas_dia = ventas_dia.filter(sell__region=reg)

        x_labels = []
        y_labels = []

        for venta in ventas_dia:
            x_labels.append(venta['day'].strftime('%Y-%m-%d'))
            y_labels.append(int(venta['total_ventas']))

        return {"dates":x_labels, "totals": y_labels}

    def form_valid(self, form):
        form_dates = form.cleaned_data
        sdate = form_dates['start_date']
        edate = form_dates['end_date']

        if sdate > edate:
            return self.form_invalid(form)

        sales = self.sales_by_range(sdate, edate)

        contexto = self.get_context_data(form=form, datos_formulario=sales)
        return self.render_to_response(contexto)

    def form_invalid(self, form):
        errors = form.errors.as_data()
        form.add_error('end_date', 'La fecha no puede ser mas grande!')
        return self.render_to_response(self.get_context_data(form=form, errors=errors))


# Create your views here.
class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('authenticate:login')
    template_name = 'inicio.html'

    def get_filter_region(self):
        user = self.request.user
        region = user.region
        if user.groups.filter(name="Director general").exists():
            return None
        return region


    def get_overview(self):
        # first batch of queries
        reg = self.get_filter_region()
        cats = Categoria.objects.count()
        prods = Producto.objects.count()
        regs = Region.objects.count()

        # second query
        completed_sales = Venta.objects.values('sell_state').annotate(count=Count('sell_state'))
        if reg:
            completed_sales = completed_sales.filter(region=reg)

        # create a dictionary that counts how many trues and falses there are.
        states = {str(estado['sell_state']): estado['count'] for estado in completed_sales}

        return {
            "categories": cats,
            "products": prods,
            "regions": regs,
            "sale_states": states,
        }

    def get_sales_overview(self):
        curr_year = timezone.now().year
        curr_month = timezone.now().month-1
        reg = self.get_filter_region()

        # FIRST QUERY: sales per current year and month
        sales_year = (
            DetalleVenta.objects
            .filter(sell__sell_date__year=curr_year)
            .annotate(month=ExtractMonth('sell__sell_date'))
            .values('month').annotate(total=Sum(F('qty') * F('price')))
            .order_by('month')
        )
        if reg:
            sales_year = sales_year.filter(sell__region=reg)

        sales_months = [int(res.get('total')) for res in sales_year]

        # SECOND QUERY: sales by region
        sales_by_region = None
        if not reg:
            sales_details = (
                DetalleVenta.objects
                .filter(sell__sell_date__year=curr_year)
            )
            sales_by_region = (
                sales_details
                .values('sell__region__name')
                .annotate(total_sales=Sum(F('qty') * F('price')))
                .order_by('-total_sales')[:10]
            )

        # THIRD QUERY: top 10 products
        sells_cyear = Venta.objects.filter(sell_date__year=curr_year)

        if reg:
            sells_cyear = sells_cyear.filter(region=reg)

        top_prods = (
            Producto.objects.filter(detalleventa__sell__in=sells_cyear) 
            .annotate(total_vendido=Sum('detalleventa__qty')) 
            .annotate(total_venta=F('total_vendido') * F('price')) 
            .order_by('-total_vendido')[:10]
        )

        # FOURTH QUERY: % of sales by category
        sales_per_cat = (
            DetalleVenta.objects
            .filter(sell__sell_date__year=curr_year)
            .values('product__category__name')
            .annotate(total_sales=Sum('qty'))
        )

        if reg:
            sales_per_cat = sales_per_cat.filter(sell__region=reg)

        total_sales = sum(sale['total_sales'] for sale in sales_per_cat)
        sales_percentages = []

        for sale in sales_per_cat:
            percentage = (sale['total_sales'] / total_sales) * 100
            sales_percentages.append({
                'name': sale['product__category__name'],
                'y': round(percentage, 4)
            })

        return {
            # first query
            "total_current_year": sum(sales_months),
            "total_current_month": sales_months[curr_month],
            "total_each_month": sales_months,
            # second query
            "total_by_region": sales_by_region,
            # third query
            "top_products": top_prods,
            # fourth query
            "total_by_categories": sales_percentages
        }


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.request.user.groups.all()
        if group:
            group = group[0]

        context['overview'] = self.get_overview()
        context['sales'] = self.get_sales_overview()
        context['region'] = self.get_filter_region() or "N/A"
        context['group'] = group

        return context
