import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class orderFilter(django_filters.FilterSet):
    date_start = DateFilter(field_name='date_ordered', lookup_expr='gte')
    date_end = DateFilter(field_name='date_ordered', lookup_expr='lte')
    note_filter = CharFilter(field_name='note', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = ['product', 'status', 'product__category']
        exclude = ['customer', 'date_ordered', 'note']