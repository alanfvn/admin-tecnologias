from django.forms import *


class ReportForm(Form):
    start_date = DateField(widget=DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))

    end_date = DateField(widget=DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))
