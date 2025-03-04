"""This module contains the views for the expenses table."""
from system_core_1.models.user_profile import UserProfile
from system_core_1.models.expenses import Expenses
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


@login_required
def expenses(request):
    """This function returns the expenses page."""
    if request.method == 'POST':
        username = request.POST.get('user')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('date')

        try:
            user = UserProfile.objects.get(username=username)
            Expenses.objects.create(user=user, amount=amount, description=description, date=date, category=category)
            messages.success(request, 'Expense added successfully')
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(username=username, groups='expense_holders',
                                       email="{}@hafeez.net".format(username))
            user = UserProfile.objects.get(username=username)
            Expenses.objects.create(user=user, amount=amount, description=description, date=date, category=category)
            messages.success(request, 'Expense added successfully')
        return redirect('cost_and_expenses')
    return redirect('cost_and_expenses')


@login_required
def get_total_expenses(request):
    """This function returns the total expenses."""
    if request.method == 'GET':
        total_expenses = Expenses.total_expenses()
        return JsonResponse({'total_expenses': total_expenses})
    return JsonResponse({'error': 'Invalid request.'})

        