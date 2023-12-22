#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the UserProfileForm class, which is used to dynamically create
the user profile form to allow users to update their profile information
"""
from django import forms
from ..models.user_profile import UserProfile


class UserProfileForm(forms.ModelForm):
    """The `UserProfileForm` class is responsible for handling the update of a user's
    profile information.
    """
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'location',
                  'user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser',
                  'date_joined', 'last_login', 'username']