from ..models.customer_details import CustomerData
from django.utils import timezone
from django import forms


class CustomerDataForm(forms.ModelForm):
    """The `CustomerDataForm` class is responsible for handling the update of a customer's
    data.
    """
    class Meta:
        model = CustomerData
        fields = ['created_at', 'update_at', 'customer_name', 'national_id',
                  'customer_contact', 'second_contact', 'first_witness_name',
                  'witness_id_no', 'first_witness_contact', 'second_witness_name',
                  'second_witness_contact', 'customer_location', 'nearest_school',
                  'nearest_market_church_hospital', 'customer_email', 'workplace',
                  'employer_or_coleague', 'employer_or_coleague_contact',
                  'account_name']
        