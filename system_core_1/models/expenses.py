"""This module contains the model for the expenses table in the database."""
from django.db import models
from .user_profile import UserProfile


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