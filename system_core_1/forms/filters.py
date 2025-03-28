#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the filters for easy
search and filtering of the data.
"""
import django_filters
from ..models.main_storage import MainStorage
from ..models.agent_profile import AgentProfile
from ..models.user_profile import UserProfile
from django import forms
from django.utils import timezone


class FilterMainStorege(django_filters.FilterSet):
    """Filter for the main storage."""
    class Meta:
        model = MainStorage
        fields = ('in_stock', 'assigned', 'phone_type',)


class FilterAgentAndData(forms.Form):
    """Filter for the agent and data."""

    user = forms.ModelChoiceField(
        queryset=AgentProfile.objects.all().order_by('id'),
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose agent',
                'required': 'required',
            }
        )
    )


class FilterAgentAndDataSales(forms.Form):

    """Filter for the agent and data."""
    current_month = timezone.now().date().month
    user = forms.ModelChoiceField(
        queryset=AgentProfile.objects.all().order_by('id'),
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose agent'
            }
        )
    )

    month = forms.ChoiceField(
        choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
                 ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'),
                 ('10', 'October'), ('11', 'November'), ('12', 'December')],
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose month',
                'required': 'required',
            }
        ),
        initial=str(current_month)
    )
    
    year = forms.ChoiceField(
        choices=[(timezone.now().date().year, timezone.now().date().year),
                 (timezone.now().date().year - 1, timezone.now().date().year - 1),
                 (timezone.now().date().year - 2, timezone.now().date().year - 2),
                 (timezone.now().date().year - 3, timezone.now().date().year - 3),
                 (timezone.now().date().year - 4, timezone.now().date().year - 4)],
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose year',
                'required': 'required',
            }
        )
    )


class FilterAgentAndDataStockOut(forms.Form):
    """Filter for the agent and data."""
    current_month = timezone.now().date().month
    month = forms.ChoiceField(
        choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
                 ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'),
                 ('10', 'October'), ('11', 'November'), ('12', 'December')],
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose month',
                'required': 'required',
            }
        ),
        initial=str(current_month)
    )
    
    year = forms.ChoiceField(
        choices=[(timezone.now().date().year, timezone.now().date().year),
                 (timezone.now().date().year - 1, timezone.now().date().year - 1),
                 (timezone.now().date().year - 2, timezone.now().date().year - 2),
                 (timezone.now().date().year - 3, timezone.now().date().year - 3),
                 (timezone.now().date().year - 4, timezone.now().date().year - 4)],
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose year',
                'required': 'required',
            }
        )
    )


class FilterSalesAndStock(forms.Form):
    """Filter for the sales and stock."""
    user = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(agentprofile__is_agent=True).all().order_by('id'),
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose agent',
            }
        )
    )
    month = forms.ChoiceField(
        choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
                 ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'),
                 ('10', 'October'), ('11', 'November'), ('12', 'December')],
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose month',
            }
        ),
        initial=str(timezone.now().date().month)
    )

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose date',
                'type': 'date',
            }
        ),
        initial=timezone.now().date()
    )
    
    year = forms.ChoiceField(
        choices=[(timezone.now().date().year, timezone.now().date().year),
                 (timezone.now().date().year - 1, timezone.now().date().year - 1),
                 (timezone.now().date().year - 2, timezone.now().date().year - 2),
                 (timezone.now().date().year - 3, timezone.now().date().year - 3),
                 (timezone.now().date().year - 4, timezone.now().date().year - 4)],
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose year',
            }
        )
    )