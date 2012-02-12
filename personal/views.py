from django import forms
from django.shortcuts import render_to_response

from porkpy.personal.models import Account

class ContactForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    
    bert = forms.CharField(required=True, help_text="this is some help text")
    ernie = forms.CharField(required=False, help_text="this is some help text")

    
class TransactionFileForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    
    upload_file = forms.FileField(required=True, help_text="File to upload")
    account = forms.ChoiceField(required=True, help_text="select account to upload transactions to")    
    
    def __init__(user, *args, **kwargs):
        super(TransactionFileForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['account'].choices = Account.objects.filter(user = self.user)
    
    
def form_test(request):
    form = ContactForm()
    return render_to_response('form.html', {'form': form})


def initial_file_process(description):
    transaction_category = next((transaction_category.category for transaction in transaction_category.objects.filter() if transaction.match in description), None)
    
    return transaction_category

#----------------------------------------------------------------------
def chart_monthly_expenditure(request, date_range):
    """
    
    """
    return

def chart_income_expendature(request, date_range):
    """
    double line graph
    """
    return

def chart_budget_comparison(request, date_range):
    """
    two comparitive pie charts split by category
    """
    return

def chart_budget(request, date_range):
    """
    
    """
    return

    
'''
interium import - import all trasactions and list, allowing selection of category for each

bonus filtering
'''