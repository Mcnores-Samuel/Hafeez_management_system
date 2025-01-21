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