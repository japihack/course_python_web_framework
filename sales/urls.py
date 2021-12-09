from django.urls import path
from .views import home_view, SaleListView, SaleDetailView

app_name = 'sales'

sales_patterns = ([
    path('', home_view, name='home'),
    path('sales/', SaleListView.as_view(), name='list'),
    path('detail/<pk>', SaleDetailView.as_view(), name='detail'),
], app_name)