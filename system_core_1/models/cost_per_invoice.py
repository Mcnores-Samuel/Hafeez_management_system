"""This model represent the cost per invoice in the system."""
from django.db import models
from system_core_1.models.main_storage import MainStorage
from django.conf import settings
from django.utils import timezone


class CostPerInvoice(models.Model):
    """This model represent the cost per invoice in the system.

    Attributes:
        partner: A foreign key to the user model.
        invoice_number: A char field to store the invoice number.
        invoice_date: A date field to store the invoice date.
        total_items: An integer field to store the total items in the invoice.
        total_cost: A float field to store the total cost of the invoice.
        total_sales: A float field to store the total sales of the invoice.
        items: A many to many field to store the items in the invoice.
        created_at: A date time field to store the date and time the invoice was created.
        updated_at: A date time field to store the date and time the invoice was updated.
        is_paid: A boolean field to store if the invoice is paid.
        date_paid: A date field to store the date the invoice was paid.
        last_payment_amount: A float field to store the last payment amount.
        last_payment_date: A date field to store the last payment date.
        last_payment_method: A char field to store the last payment method.
        current_balance: A float field to store the current balance.
        total_paid: A float field to store the total amount paid.
    """
    partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice_number = models.CharField(auto_created=True, max_length=15, unique=True)
    invoice_date = models.DateField(auto_created=True)
    total_invoice_items = models.IntegerField(default=0)
    original_cost = models.FloatField(default=0.00)
    cost_per_ex_rate = models.FloatField(default=0.00)
    total_items_sold = models.IntegerField(default=0)
    items = models.ManyToManyField(MainStorage, related_name='invoice_items')
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateField(default=None, null=True)
    last_payment_amount = models.FloatField(default=0.00)
    last_payment_date = models.DateField(auto_created=True)
    last_payment_method = models.CharField(max_length=15, default='Bank Transfer')
    current_balance = models.FloatField(default=0.00)
    total_amount_paid = models.FloatField(default=0.00)

    def attach_items(self, inventory_items):
        """This method is used to attach an item to the invoice.

        Args:
            inventory_items: A list of inventory items to attach to the invoice
        """
        self.items.add(*inventory_items)
        self.total_invoice_items = self.items.count()
        self.original_cost = sum([item.cost for item in self.items.all()])
        self.invoice_number = f'HAFEEZ/INV-{self.pk}'
        self.save()

    def detach_items(self, inventory_items):
        """This method is used to detach an item from the invoice.

        Args:
            inventory_items: A list of inventory items to detach from the invoice
        """
        self.items.remove(*inventory_items)
        self.total_invoice_items = self.items.count()
        self.original_cost = sum([item.cost for item in self.items.all()])
        self.save()
    
    def get_invoice_items(self):
        """This method is used to get the items in the invoice.
        """
        return self.items.all()

    def __str__(self):
        return self.invoice_number
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Cost Per Invoice'
        verbose_name_plural = 'Cost Per Invoices'
        db_table = 'cost_per_invoice'
        managed = True
        app_label = 'system_core_1'



class DailyExchangeRate(models.Model):
    """This model represent the daily exchange rate in the system.

    Attributes:
        date: A date field to store the date of the exchange rate.
        exchange_rate: A decimal field to store the exchange rate.
    """
    date = models.DateTimeField(default=timezone.now)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.date} - {self.exchange_rate}'
    

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Daily Exchange Rate'
        verbose_name_plural = 'Daily Exchange Rates'
        db_table = 'daily_exchange_rate'
        managed = True
        app_label = 'system_core_1'