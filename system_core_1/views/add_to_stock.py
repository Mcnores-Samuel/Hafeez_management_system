"""This module contains a view function for adding phones to stock."""
from django.shortcuts import render, redirect
from ..forms.add_to_stock import AddToStockForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def add_to_stock(request):
    """This view function is responsible for handling the addition of phones to stock.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Renders the add to stock form.
    - If the form is submitted, the phone is added to stock.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it renders the add to stock form.

    Usage:
    Agents access this view to add phones to stock.
    It ensures that only agents are able to access this view.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='staff_members').exists():
        if request.method == 'POST':
            form = AddToStockForm(request.POST)
            if form.is_valid():
                form.process()
                messages.success(request, 'Phone added to stock successfully.')
                return redirect('dashboard')
        else:
            form = AddToStockForm()
        return render(request, 'users/staff_sites/add_to_stock.html', {'form': form})
    return render(request, '403.html')