#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module contains the forms related to the user profile."""
from django import forms


class UserAvatarForm(forms.Form):
    """Form for the user avatar."""
    avatar = forms.ImageField(label='avatar', required=False)