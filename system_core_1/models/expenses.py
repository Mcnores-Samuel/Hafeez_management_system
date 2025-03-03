"""This module contains the model for the expenses table in the database."""
from django.db import models
from .user_profile import UserProfile
from django.utils import timezone
from django.db.models import Sum


class Expenses(models.Model):
    """The model for the expenses table.

    Attributes:
        user (ForeignKey): The user who made the expense.
        amount (DecimalField): The amount of the expense.
        description (TextField): The description of the expense.
        date (DateTimeField): The date the expense was made.
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'expenses'
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        indexes = [
            models.Index(fields=['date'])
        ]
    
    @classmethod
    def total_expenses(cls):
        """Returns the total expenses."""
        total = cls.objects.filter(
            date__year=timezone.now().year,
        ).aggregate(total_expenses=Sum('amount'))
        return total['total_expenses']
    
    @classmethod
    def total_current_month_expenses(cls):
        """Returns the total expenses for the current month."""
        total = cls.objects.filter(
            date__month=timezone.now().month,
            date__year=timezone.now().year
        ).aggregate(total_expenses=Sum('amount'))
        return total['total_expenses']


class FixedAssets(models.Model):
    """The model for the fixed assets table.

    Attributes:
        name (CharField): The name of the asset.
        description (TextField): The description of the asset.
        date_purchased (DateTimeField): The date the asset was purchased.
        cost (DecimalField): The cost of the asset.
        useful_life (IntegerField): The useful life of the asset.
        salvage_value (DecimalField): The salvage value of the asset.
        depreciation (DecimalField): The depreciation of the asset.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_purchased = models.DateTimeField()
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    useful_life = models.IntegerField()
    salvage_value = models.DecimalField(max_digits=20, decimal_places=2)
    depreciation = models.DecimalField(max_digits=20, decimal_places=2)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'fixed_assets'
        verbose_name = 'Fixed Asset'
        verbose_name_plural = 'Fixed Assets'
        indexes = [
            models.Index(fields=['date_purchased'])
        ]

    @classmethod
    def total_assets_cost(cls):
        """Returns the total cost of the assets."""
        total = cls.objects.aggregate(total_cost=Sum('cost'))
        if total['total_cost'] is None:
            return 0
        return total['total_cost']
    
    @classmethod
    def total_assets_current_value(cls):
        """Returns the total current value of the assets."""
        total = cls.objects.aggregate(total_current_value=Sum('depreciation'))
        if total['total_current_value'] is None:
            return 0
        return total['total_current_value']


class Capital(models.Model):
    """The model for the capital table.

    Attributes:
        source (CharField): The source of the capital.
        amount (DecimalField): The amount of the capital.
        description (TextField): The description of the capital.
        date (DateTimeField): The date the capital was invested.
    """
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.source
    
    class Meta:
        db_table = 'capital'
        verbose_name = 'Capital Investment'
        verbose_name_plural = 'Capital Investments'
        indexes = [
            models.Index(fields=['date'])
        ]


class Liability(models.Model):
    """The model for the liability table.

    Attributes:
        type (CharField): The type of liability.
        creditor (CharField): The creditor of the liability.
        amount (DecimalField): The amount of the liability.
        description (TextField): The description of the liability.
        effective_date (DateTimeField): The date the liability commenced.
        due_date (DateTimeField): The date the liability is due.
        is_paid (BooleanField): Whether the liability has been paid.
    """
    LIABILITIES_TYPE = [
        ('current', 'Current Liability'),
        ('non_current', 'Non-Current Liability')
    ]

    type = models.CharField(max_length=255, choices=LIABILITIES_TYPE)
    creditor = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    effective_date = models.DateTimeField()
    due_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.creditor} - {self.amount}'
    
    class Meta:
        db_table = 'liabilities'
        verbose_name = 'Liability'
        verbose_name_plural = 'Liabilities'
        indexes = [
            models.Index(fields=['effective_date'])
        ]

    @classmethod
    def total_current_liabilities(cls):
        """Returns the total current liabilities."""
        total = cls.objects.filter(
            type='current',
            is_paid=False
        ).aggregate(total_current_liabilities=Sum('amount'))
        if total['total_current_liabilities'] is None:
            return 0
        return total['total_current_liabilities']
    
    @classmethod
    def total_non_current_liabilities(cls):
        """Returns the total non-current liabilities."""
        total = cls.objects.filter(
            type='non_current',
            is_paid=False
        ).aggregate(total_non_current_liabilities=Sum('amount'))
        if total['total_non_current_liabilities'] is None:
            return 0
        return total['total_non_current_liabilities']