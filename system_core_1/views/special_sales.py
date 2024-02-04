"""This module contains the views related to the special sales."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models.special_orders import SpecialOrders
from ..models.reference import Price_reference
from ..models.main_storage import MainStorage


@login_required
def special_sales(request):
    return render(request, 'users/admin_sites/special_sales.html')