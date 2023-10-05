#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the filters for easy search and filtering of the data."""
import django_filters
from ..models.main_storage import MainStorage
from ..models.agent_profile import AgentProfile

class FilterMainStorege(django_filters.FilterSet):
    """Filter for the main storage."""
    class Meta:
        model = MainStorage
        fields = ('in_stock', 'assigned', 'phone_type', 'entry_date')

class FilterAgentAndData(django_filters.FilterSet):
    """Filter for the agent and data."""
    class Meta:
        model = AgentProfile
        fields = ('user', )