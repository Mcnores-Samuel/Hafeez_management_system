#!/usr/bin/env python3
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


PHONELIST = (
        ("S18 (4+64)", "S18 (4+64)"), ("A60 (2+32)", "A60 (2+32)"),
        ("A04 (2+32)", "A04 (2+32)"), ("A18 (1+32)", "A18 (1+32)"),
        ("Camon 20 (8+256)", "Camon 20 (8+256)"), ("Camon 19 (4+128)", "Camon 19 (4+128)"),
        ("Spark 10 (8+128)", "Spark 10 (8+128)"), ("Spark 10C (8+128)", "Spark 10C (8+128)"),
        ("Spark 10C (4+128)", "Spark 10C (4+128)"), ("Spark 8C (2+64)", "Spark 8C (2+64)"),
        ("Pop 7 pro (4+64)", "Pop 7 pro (4+64)"), ("Pop 7 pro (3+64)", "Pop 7 pro (3+64)"),
        ("Pop 7 (2+64)", "Pop 7 (2+64)"),

    )

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractUser):
  email = models.EmailField(max_length=100, unique=True)
  phone_number = models.CharField(max_length=15, blank=True, null=True)
  objects = UserProfileManager()
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email
  



class AgentProfile(models.Model):
  """The Agents model represents the individuals who facilitate the sales
  process. It includes fields to store relevant information about each agent,
  such as their name and email address
  """
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  is_agent = models.BooleanField(default=True)

  def __str__(self):
      return self.user.username


class AgentStock(models.Model):
    """
    The AgentStock model represents the inventory of phones assigned to agents
    within the application. It tracks the availability and status of phones
    assigned to specific agents.

    Fields:
    - agent: A foreign key reference to the AgentProfile of the assigned agent.
    - imei_number: The International Mobile Equipment Identity (IMEI) number of
      the phone, serving as a unique identifier.
    - phone_type: The type or model of the phone.
    - collection_date: The date on which the phone was collected by the agent.
    - sales_type: The type of sale (e.g., cash or loan) for the phone.
    - in_stock: A boolean field indicating whether the phone is currently in stock
      and available for assignment to agents.
    
    Usage:
    The AgentStock model plays a vital role in managing the allocation of phones to
    agents. It helps track which phones are assigned to which agents, their collection
    dates, sales types, and overall availability.

    Note:
    - Properly managing the AgentStock model ensures that agents have access to the
      phones they need for sales.
    - Changes to the assignment, collection, or availability of phones should be
      accurately recorded in this model.
    """
    TYPES = (
        ("Cash", "Cash"),
        ("Loan", "Loan"),
    )
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    imei_number = models.CharField(max_length=15, unique=True)
    phone_type = models.CharField(max_length=25, blank=True)
    collection_date = models.DateField()
    sales_type = models.CharField(max_length=10, choices=TYPES, default="Loan")
    contract_number = models.CharField(max_length=8,null=True)
    in_stock = models.BooleanField(default=True)
    stock_out_date = models.DateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Dynamically populate choices for imei_number from MainStorage"""
        self._update_imei_number_choices()

    def _update_imei_number_choices(self):
        in_stock_phones = MainStorage.objects.filter(in_stock=True)
        choices = [(phone.device_imei, phone.device_imei) for phone in in_stock_phones]
        self._meta.get_field('imei_number').choices = choices


class CustomerData(models.Model):
    """The Customers table serves as a central repository for customer-related
    information gathered during the phone purchasing process. Each customer
    record is uniquely identified by a generated customer_id, and the
    associated timestamp indicates when the data was collected.

    Contact information is collected through customer_contact and
    second_contact fields, allowing for multiple points of communication.
    Witness information is recorded in first_witness_name,
    first_witness_contact,second_witness_name, and second_witness_contact
    fields to provide additional verification.

    Location-related details are captured, including customer_location,
    nearest_school, and nearest_market_church_hospital, aiding in logistics
    and customer service.

    customer_email allows for electronic communication with the customer.
    The contract_number links the customer to a specific contract, and referral
    captures any relevant referral information.

    The Customers table forms an essential part of the database, enabling
    effective management of customer data, tracking interactions, and
    maintaining accurate records of customers engaged in your loan-based
    phone sales program.
    """
    created_at = models.DateTimeField(null=True)
    update_at = models.DateTimeField()
    customer_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=9)
    customer_contact = models.CharField(max_length=13)
    second_contact = models.CharField(max_length=13, null=True)
    first_witness_name = models.CharField(max_length=50)
    first_witness_contact = models.CharField(max_length=13)
    second_witness_name = models.CharField(max_length=50)
    second_witness_contact = models.CharField(max_length=13)
    customer_location = models.CharField(max_length=50)
    nearest_school = models.CharField(max_length=50)
    nearest_market_church_hospital = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = 'cryptic_core_app' 


class phone_reference(models.Model):
    """This model holds static information on phone's payment methods.

    The PhoneReference model represents reference data for different phone models
    available for sale. It serves as a catalog of phones, including their specifications
    and pricing information. This model is essential for managing and organizing the
    inventory of phones in your application.

    Fields:
    - phone: The name or model of the phone.
    - merchant_price: The price at which the phone is sold to merchants or agents.
    - deposit: The initial deposit amount required for purchasing the phone.

    Usage:
    The PhoneReference model is primarily used for maintaining a centralized database
    of available phone models and their associated details. It allows for easy retrieval
    of phone information when agents or users need to select a phone for sale.

    Note:
    - This model should be populated with relevant phone data, including new phone
      models and their specifications.
    - The data in this model can be used for pricing, cataloging, and displaying phone
      options to agents and customers.
    - Changes to this model can affect the phone selection process in the application,
      so it should be kept up-to-date and accurate.
    """
    phone = models.CharField(max_length=30)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    merchant_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'cryptic_core_app'
    
    def __str__(self):
        """String representation of the phone reference model"""
        return ("{} {} {}".format(self.phone, self.deposit, self.merchant_price))
    
    @classmethod
    def get_all_phones(cls):
        return cls.objects.all()


class PhoneData(models.Model):
    """The PhoneData model establishes a relationship with the Customers and
    Agents models through foreign key fields (customer and agent respectively)
    This allows each phone record to be linked to the corresponding customer
    and agent.

    The model also includes fields to capture specific details about the phone
    purchase, such as phone_type, imei_number, selling_price, cost_price,
    payment_period, and deposit.
    """
    customer = models.ForeignKey(CustomerData, on_delete=models.CASCADE)
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    phone_type = models.CharField(max_length=25, choices=PHONELIST, default='S18 (4+64)')
    imei_number = models.CharField(max_length=15, unique=True)
    contract_number = models.CharField(max_length=8,null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_period = models.CharField(max_length=50, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    class Meta:
        app_label = 'cryptic_core_app'


class MainStorage(models.Model):
    """This model represent the entire stock available and sold in all posts.

    The MainStorage model represents the primary storage for phones available
    in your application. It serves as the central repository for tracking phone
    inventory and availability.

    Fields:
    - device_imei: The International Mobile Equipment Identity (IMEI) number,
      which serves as a unique identifier for each phone.
    - phone_type: The type or model of the phone.
    - in_stock: A boolean field indicating whether the phone is currently in stock
      and available for sale.
    - assigned: A boolean field indicating whether the phone is currently assigned
      to an agent or customer.
    - stock_out_date: The date on which the phone was purchased or added to the
      inventory.

    Usage:
    The MainStorage model plays a crucial role in managing the availability and
    tracking of phones within your application. It helps ensure that phones are in
    stock, available for assignment, and properly recorded.

    Note:
    - Properly maintaining the MainStorage model is essential for accurate inventory
      management.
    - Changes to the availability or assignment of phones should be reflected in this
      model to ensure accurate tracking.
    """
    device_imei = models.CharField(max_length=15, unique=True)
    phone_type = models.CharField(max_length=25, choices=PHONELIST, default='S18 (4+64)')
    in_stock = models.BooleanField(default=True)
    sales_type = models.CharField(max_length=10, null=True)
    contract_no = models.CharField(max_length=8, null=True)
    entry_date = models.DateField()
    stock_out_date = models.DateField()
    assigned = models.BooleanField(default=False)
    