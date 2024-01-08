"""This module contains the commission model,
which is used to store the commission

This is the agents commission earned from the sales of phones
over a period of time a month or a week
"""
from django.db import models
from django.utils import timezone
from .user_profile import UserProfile


class Commission(models.Model):
    agent = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)
    total_devies_sold = models.IntegerField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    month = models.CharField(
        max_length=20,
        default=timezone.now().date().month)
    year = models.CharField(
        max_length=20,
        default=timezone.now().date().year)
    paid = models.BooleanField(default=False)

    def __str__(self):
        """Return a string representation of the model."""
        return "Commission for {} {} {}".format(
            self.agent, self.month, self.year)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Commissions'
        unique_together = ('agent', 'month', 'year')