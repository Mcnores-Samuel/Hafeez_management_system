"""This module contains the model for the final sales table in the database.

Attributes:
"""
from django.db import models
from .user_profile import UserProfile
from django.utils import timezone


class AccountManager(models.Model):
    """The model for the account manager table.
    The account manager table contains the details of the account manager
    responsible for managing user accounts and contracts.

    Attributes:
        mbo (ForeignKey): The user profile of the account manager.
        contract (CharField): The contract number of the account manager.
        date_created (DateTimeField): The date the account manager was created.
        date_updated (DateTimeField): The date the account manager was last updated.
        active (BooleanField): Indicates if the account manager is active.
        approved (BooleanField): Indicates if the account manager is approved.
        rejected (BooleanField): Indicates if the account manager is rejected.
        issue (BooleanField): Indicates if the account manager has an issue.
        rejected_reason (TextField): The reason for rejecting the account manager.
        rejected_proof (ImageField): The proof of rejection for the account manager.
    """
    mbo = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    contract = models.CharField(max_length=9, blank=True, null=True)
    device_imei = models.CharField(max_length=15, blank=True, null=True)
    device_name = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=50, blank=True, null=True)
    payg_number = models.CharField(max_length=15, blank=True, null=True)
    date_created = models.DateTimeField(timezone.now())
    date_updated = models.DateTimeField(timezone.now())
    date_approved = models.DateTimeField(timezone.now())
    locked = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    rejected = models.BooleanField(default=False)
    issue = models.BooleanField(default=False)
    resolved = models.BooleanField(default=True)
    important_note = models.TextField(blank=True, null=True)
    rejected_reason = models.TextField(blank=True, null=True)
    issue_description = models.TextField(blank=True, null=True)
    rejected_proof = models.ImageField(upload_to='rejected_proof/', blank=True, null=True)
