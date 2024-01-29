"""This module contains the form for adding phones to stock."""
from django import forms
from ..models.main_storage import MainStorage
from ..models.user_profile import UserProfile
from django.contrib.auth.models import Group
from django.utils import timezone


class AddToStockForm(forms.Form):
    """This class contains the form for adding phones to stock.
    
    Attributes:
        device_imei (CharField): The IMEI number of the phone.
        device_imei_2 (CharField): The IMEI number of the phone.
        name (CharField): The name of the phone.
        supplier (CharField): The name of the supplier.
    
    Functions:
        __init__: Initializes the form.
        clean: Validates the form data.
        process_data: Processes the form data and saves it to the database.

    Note:
        This form is used in the add_to_stock view.
    """
    device_imei = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter IMEI number',
                'required': 'required',
                'minlength': '15',
                'maxlength': '15',
                'autofocus': 'autofocus',
            }
        )
    )
    device_imei_2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter IMEI number 2',
                'required': 'required',
                'minlength': '15',
                'maxlength': '15',
            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone name',
                'required': 'required',
                'list': 'phone_list',
            }
        )
    )
    supplier = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        """Override the init method to get the user."""
        self.user = kwargs.pop('user', None)
        super(AddToStockForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Override the clean method to ensure that the IMEI numbers are unique."""
        cleaned_data = super().clean()
        device_imei = cleaned_data.get('device_imei')
        device_imei_2 = cleaned_data.get('device_imei_2')
        check = device_imei.isdigit()
        check_2 = device_imei_2.isdigit()
        if not check and len(device_imei) != 15:
            raise forms.ValidationError("IMEI 1 number must be digits up to 15 characters")
        if not check_2 and len(device_imei_2) != 15:
            raise forms.ValidationError("IMEI 2 number must be digits up to 15 characters")
        if MainStorage.objects.filter(device_imei=device_imei).exists():
            raise forms.ValidationError("IMEI 1 number already exists")
        if MainStorage.objects.filter(device_imei_2=device_imei_2).exists():
            raise forms.ValidationError("IMEI 2 number already exists")
        if device_imei == device_imei_2:
            raise forms.ValidationError("IMEI numbers must be unique")
        return cleaned_data
    
    def process_data(self):
        """Process the form data and save it to the database."""
        main_shop_staff = Group.objects.get(name='main_shop')
        representatives = UserProfile.objects.filter(groups=main_shop_staff)
        agent = representatives.first()
        device = None
        if self.cleaned_data['name'] == 'Spark 10C':
            device = MainStorage.objects.filter(
                name=self.changed_data['name'],
                phone_type='10C').first()
        else:
            device = MainStorage.objects.filter(
                name__exact=self.cleaned_data['name']).first()
        if device:
            stock = MainStorage.objects.create(
                device_imei=self.cleaned_data['device_imei'],
                device_imei_2=self.cleaned_data['device_imei_2'],
                name=self.cleaned_data['name'],
                phone_type=device.phone_type,
                category=device.category,
                spec=device.spec,
                screen_size=device.screen_size,
                os=device.os,
                battery=device.battery,
                camera=device.camera,
                supplier=self.cleaned_data['supplier'],
                agent=agent,
                recieved=True,
                assigned=True,
                in_stock=True,
                sold=False,
                contract_no='##',
                sales_type='##',
                entry_date=timezone.now(),
                stock_out_date=timezone.now(),
                collected_on=timezone.now(),
                assigned_from='HAFEEZ ENTERPRISE',
                updated_by=self.user.username,
            )
            stock.save()
            return stock
