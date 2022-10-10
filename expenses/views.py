from django.views.generic.list import ListView

from .forms import UpgradedForm
from .models import Expense, Category
from .reports import summary_per_category, total_expanses, summary_per_month, expenses_count_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = UpgradedForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            datefrom = form.cleaned_data.get('datefrom', '')
            dateto = form.cleaned_data.get('dateto', '')
            category = form.cleaned_data.get('category', '')
            sort_by = form.cleaned_data.get('sort_by', '')

            if category:
                queryset = queryset.filter(category=category)
            if datefrom:
                queryset = queryset.filter(date__gte=datefrom)
            if dateto:
                queryset = queryset.filter(date__lte=dateto)
            if name:
                queryset = queryset.filter(name__icontains=name)
            if sort_by:
                queryset = queryset.order_by(sort_by)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_expanses=total_expanses(queryset),
            summary_per_month=summary_per_month(queryset),
            **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        
        return super().get_context_data(
            object_list=queryset,
            expenses_count_per_category=expenses_count_per_category(queryset),
            **kwargs)

