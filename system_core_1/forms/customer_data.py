#!/usr/bin/env python3
from django import forms
from ..models.reference import Price_reference
from ..models.main_storage import MainStorage
from ..models.customer_details import CustomerData
from ..models.customer_order import PhoneData
from django.utils import timezone


class CombinedDataForm(forms.Form):
    """
    The CombinedDataForm is a Django form used for collecting and processing
    combined customer and phone data during the phone purchasing process.

    This form allows the user, typically an agent, to gather essential customer
    information and select a phone for sale. It is designed to facilitate the
    creation of customer and phone records simultaneously in the database.

    Form Fields:
    - Customer Information:
      - customer_name: Full name of the customer.
      - national_id: National identification number of the customer.
      - customer_contact: Primary contact number of the customer.
      - second_contact: Secondary contact number of the customer (optional).
      - first_witness_name: Name of the first witness.
      - first_witness_contact: Contact number of the first witness.
      - second_witness_name: Name of the second witness.
      - second_witness_contact: Contact number of the second witness.
      - customer_location: Customer's residential location.
      - nearest_school: Nearest school to the customer's location.
      - nearest_market_church_hospital: Nearest market, church, or hospital.
      - customer_email: Customer's email address (optional).

    - Phone Selection:
      - phone_type: Choice field for selecting the type of phone.
      - imei_number: Unique identification number of the selected phone.
      - payment_period: Payment period or plan for the phone.
    
    Methods:
    - __init__: Initializes the form, sets choices for phone_type based on
      available phone references, and dynamically sets choices for imei_number
      based on the agent's available stock.
    - save: Processes and saves the combined data, creating customer and phone
      records in the database.

    Usage:
    Agents or users can fill out this form to gather customer data and select a
    phone for sale. Upon submission, the form saves both customer and phone
    records in the database, facilitating efficient management of customer
    information and phone sales.

    Note:
    This form is typically used in a view where user authentication and data
    validation are handled.
    """
    PAYMENT = [
        ('Cash', 'Cash'),
        ('Loan', 'Loan'),
    ]

    PAYMENT_PERIOD = [
        ('6 Months', '6 Months'),
        ('12 Months', '12 Months'),

    ]

    customer_data = None
    phone_data = None
    main_storage_phone = None
    agent_stock_phone = None

    payment_method = forms.ChoiceField(choices=PAYMENT, widget=forms.RadioSelect, required=True)
    customer_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Enter customer's full name."}))
    national_id = forms.CharField(max_length=9, required=False, widget=forms.TextInput({ "placeholder": "National identification number."}))
    customer_contact = forms.CharField(max_length=13, required=False, widget=forms.TextInput({ "placeholder": "Primary contact number"}))
    second_contact = forms.CharField(max_length=13, required=False, widget=forms.TextInput({ "placeholder": "A secondary contact number.(optional)"}))
    first_witness_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "First witness full name"}))
    witness_id_no = forms.CharField(max_length=9, required=False, widget=forms.TextInput({ "placeholder": "First witness national ID number"}))
    first_witness_contact = forms.CharField(max_length=13, required=False, widget=forms.TextInput({ "placeholder": "First witness primary contact"}))
    second_witness_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Second witness full name"}))
    second_witness_contact = forms.CharField(max_length=13, required=False, widget=forms.TextInput({ "placeholder": "Second witness primary contact"}))
    customer_location = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Customer's based location"}))
    nearest_school = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Nearest school if any"}))
    nearest_market_church_hospital = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Nearest market, church or hospital if any"}))
    customer_email = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Customer's email address"}))
    payment_period = forms.ChoiceField(choices=PAYMENT_PERIOD, required=False, widget=forms.RadioSelect)
    workplace = forms.CharField(max_length=100, required=False, widget=forms.TextInput({ "placeholder": "Customer's workplace"}))
    employer_or_coleague = forms.CharField(max_length=100, required=False, widget=forms.TextInput({ "placeholder": "Customer's employer or coleague"}))
    employer_or_coleague_contact = forms.CharField(max_length=13, required=False, widget=forms.TextInput({ "placeholder": "Customer's employer or coleague contact"}))


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        if payment_method == 'Loan':
            required_fields = [
                'customer_name', 'national_id', 'customer_contact',
                'first_witness_name', 'first_witness_contact', 'payment_period',
                'customer_location', 'nearest_school', 'nearest_market_church_hospital'
            ]
            for field_name in required_fields:
                field_value = cleaned_data.get(field_name)
                if not field_value:
                    if field_name == 'payment_period':
                        self.add_error(field_name, 'Please select a payment period')
                    elif field_name == 'customer_name':
                        self.add_error(field_name, 'Please enter customer name')
                    elif field_name == 'national_id':
                        self.add_error(field_name, 'Please enter customer national ID')
                    elif field_name == 'customer_contact':
                        self.add_error(field_name, 'Please enter customer contact')
                    elif field_name == 'first_witness_name':
                        self.add_error(field_name, 'Please enter first witness name')
                    elif field_name == 'first_witness_contact':
                        self.add_error(field_name, 'Please enter first witness contact')
                    elif field_name == 'customer_location':
                        self.add_error(field_name, 'Please enter customer location')
                    elif field_name == 'nearest_school':
                        self.add_error(field_name, 'Please enter nearest school')
                    elif field_name == 'nearest_market_church_hospital':
                        self.add_error(field_name, 'Please enter nearest market, church or hospital')
        return cleaned_data

    def process_cash_payment(self, data_id):
        """
        The process_cash_payment function is responsible for processing a
        payment when the selected payment method is "Cash." In this scenario, customer
        data is not collected, and the function focuses on creating phone data records
        for the transaction.
        
        Functionality:
                Retrieves the relevant information about the selected phone and phone reference.
                Creates a phone data record in the database, capturing details such as the agent,
                IMEI number, phone type, selling price, deposit, and payment period.
                Returns the newly created phone data object.
        Usage:
                This function is called when a user selects "Cash" as the payment method during
                the phone purchasing process. It ensures that the transaction details are recorded
                without the need for collecting customer data.
        """
        selected_device = MainStorage.objects.get(id=data_id)
        selected_device.in_stock = False
        selected_device.sold = True
        selected_device.stock_out_date = timezone.now()
        selected_device.sales_type = 'Cash'
        selected_device.save()

    def process_loan_payment(self, data_id):
        """
        The process_loan_payment function handles the processing of a payment
        when the selected payment method is "Loan." In this case, it collects
        customer data and creates both customer and phone data records in the database.

        Functionality:
                Retrieves the relevant information about the selected phone and phone reference.
                Gathers and validates customer data, including name, national ID, contact details,
                witness information, location, email, and contract number.
                Creates a customer data record in the database with the provided customer information.
                Creates a phone data record associated with the customer, capturing details such as the agent,
                IMEI number, phone type, selling price, deposit, and payment period.
                Returns the newly created customer data and phone data objects.
        Usage:
                This function is called when a user selects "Loan" as the payment method
                during the phone purchasing process. It ensures the collection of essential customer
                data along with transaction details, facilitating customer and phone data management in the database.
        """
        check_if_sold_already = MainStorage.objects.get(id=data_id)
        if not check_if_sold_already.sold:
            selected_device = MainStorage.objects.get(id=data_id)
            phone_reference_instance = Price_reference.objects.get(
                phone=selected_device.phone_type
            )
            selected_device.in_stock = False
            selected_device.sold = True
            selected_device.sales_type = 'Loan'
            selected_device.stock_out_date = timezone.now()
            selected_device.save()

            self.user = selected_device.agent

            if selected_device:
                customer_data = CustomerData(
                    created_at=timezone.now(),
                    update_at=timezone.now(),
                    agent=self.user.agentprofile if self.user else None,
                    customer_name=self.cleaned_data['customer_name'],
                    national_id=self.cleaned_data['national_id'],
                    customer_contact=self.cleaned_data['customer_contact'],
                    second_contact=self.cleaned_data['second_contact'],
                    first_witness_name=self.cleaned_data['first_witness_name'],
                    witness_id_no=self.cleaned_data['witness_id_no'],
                    first_witness_contact=self.cleaned_data['first_witness_contact'],
                    second_witness_name=self.cleaned_data['second_witness_name'],
                    second_witness_contact=self.cleaned_data['second_witness_contact'],
                    customer_location=self.cleaned_data['customer_location'],
                    nearest_school=self.cleaned_data['nearest_school'],
                    nearest_market_church_hospital=self.cleaned_data['nearest_market_church_hospital'],
                    customer_email=self.cleaned_data['customer_email'],
                    workplace=self.cleaned_data['workplace'],
                    employer_or_coleague=self.cleaned_data['employer_or_coleague'],
                    employer_or_coleague_contact=self.cleaned_data['employer_or_coleague_contact'],
                )
                customer_data.save()

                phone_data = PhoneData(
                    customer=customer_data,
                    agent=self.user.agentprofile if self.user else None,
                    imei_number=selected_device.device_imei,
                    phone_type=selected_device.phone_type,
                    selling_price=phone_reference_instance.merchant_price,
                    deposit=phone_reference_instance.deposit,
                    payment_period=self.cleaned_data['payment_period'],
                )
                phone_data.save()
            return customer_data, phone_data
        else:
            return 'already sold', 'already sold'