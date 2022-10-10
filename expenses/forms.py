from django import forms
from .models import Expense


class ExpenseSearchForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['category'].required = False


class UpgradedForm(forms.Form, ExpenseSearchForm):
    CHOICES = (
        ('', '---------'),
        ('date', 'date ascending'),
        ('-date', 'date descending'),
        ('category', 'category ascending'),
        ('-category', 'category descending')
        )
    datefrom = forms.DateField(label="Date from:", required=False)
    dateto = forms.DateField(label="Date to:", required=False)
    sort_by = forms.ChoiceField(choices=CHOICES, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datefrom'].widget.attrs.update({'placeholder': '2021-01-22'})
        self.fields['dateto'].widget.attrs.update({'placeholder': '2021-01-22'})

        