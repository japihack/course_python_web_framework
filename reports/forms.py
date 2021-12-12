from django import forms
from .models import Report

class ReportForms(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'remarks')