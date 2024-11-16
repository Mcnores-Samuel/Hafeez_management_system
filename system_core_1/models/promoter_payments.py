"""This module contains the PromoterPayments model."""
from django.db import models
from django.utils import timezone
from .user_profile import UserProfile


class PromoterPayments(models.Model):
    """Model to store the payments made by promoters."""
    promoter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    total_mifi_paid = models.IntegerField()
    total_idu_paid = models.IntegerField()
    total_devices_paid = models.IntegerField(default=0)
    total_updated = models.IntegerField(default=0)
    updated_completed = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)
    payment_date = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)
    updated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='updated_by')

    def __str__(self):
        return f'{self.promoter.first_name} {self.promoter.last_name} - {self.amount_paid}'
    
    class Meta:
        verbose_name = 'Promoter Payment'
        verbose_name_plural = 'Promoter Payments'
        ordering = ['-payment_date']

