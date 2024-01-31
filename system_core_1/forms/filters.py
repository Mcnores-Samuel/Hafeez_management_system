#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the filters for easy
search and filtering of the data.
"""
import django_filters
from ..models.main_storage import MainStorage
from ..models.agent_profile import AgentProfile
from django import forms


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