from django.shortcuts import render
from django.utils.formats import date_format
from django.views.generic import ListView, DetailView
from sales.utils import get_customer_from_id, get_salesman_from_id
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd

# Create your views here.
def home_view(request):
    form = SalesSearchForm(request.POST or None)
    sales_df = None
    positions_df = None

    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)

        if len(sale_qs)>0:
            sales_df = pd.DataFrame(sale_qs.values())
            
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({'customer_id':'customer', 'salesman_id':'salesman', 'id':'sales_id'}, axis=1, inplace=True)
            sales_df = sales_df.to_html
            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id':pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data).to_html
        else:
            sales_df = 'No data'    

    context = {
        'form': form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        
    }
    return render(request, 'sales/home.html', context)

class SaleListView(ListView):
    model = Sale

class SaleDetailView(DetailView):
    model = Sale