from collections import OrderedDict

from django.db.models import Sum, Value, Count
from django.db.models.functions import Coalesce, TruncMonth


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def total_expanses(queryset):
    return queryset.aggregate(Sum('amount'))['amount__sum']


def summary_per_month(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(s=Sum('amount'))
        .values_list('month', 's')
        ))


def expenses_count_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .order_by()
        .values('name')
        .annotate(c=Count('expense__name'))
        .values_list('name', 'c')
    ))

