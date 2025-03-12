"""This module contains the views related to the faq."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def faq(request):
    """This function returns the faq page."""
    if request.method == 'GET':
        if request.user.is_superuser:
            return render(request, 'users/admin_sites/faq.html')
        elif request.user.groups.filter(name='branches').exists():
            return render(request, 'users/branches/faq.html')
        elif request.user.groups.filter(name='staff_members').exists():
            return render(request, 'users/staff_sites/faq.html')
        elif request.user.groups.filter(name='agents').exists():
            return render(request, 'users/agents/faq.html')
        else:
            return redirect('dashboard')
    return redirect('dashboard')