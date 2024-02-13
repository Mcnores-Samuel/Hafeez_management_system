"""This module contains the views related to the special sales."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models.special_orders import SpecialOrders
from ..models.user_profile import UserProfile
from ..models.reference import Price_reference
from ..models.main_storage import MainStorage


@login_required
def special_sales(request):
    data = SpecialOrders.objects.all().order_by('-updated_on')
    if request.method == 'POST':
        current_payment = request.POST.get('current_payment')
        stakeholder = request.POST.get('stakeholder')
        if current_payment:
            current_payment = int(current_payment)
            rep = UserProfile.objects.get(username=stakeholder)
            order = SpecialOrders.objects.get(presentative=rep)
            order.last_payment = current_payment
            order.save()
            return redirect('special_sales')
    return render(request, 'users/admin_sites/special_sales.html', {'data': data})