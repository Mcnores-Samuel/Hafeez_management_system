"""This module contains the views for handling deposit payments."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as message
from django.http import JsonResponse
from ..models.main_storage import MainStorage
from ..models.user_profile import UserProfile
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def pending_deposit_payments(request):
    """Display the pending deposit payments page."""
    if request.method == 'GET' and request.user.is_superuser:
        monday = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())
        sunday = monday + timezone.timedelta(days=6)
        data = MainStorage.objects.filter(
            stock_out_date__range=[monday, sunday], mbo_approved=True,
            in_stock=False, sold=True, recieved=True, pending=True,
            deposit_paid=False, is_locked=True, sales_type='Loan').order_by('-stock_out_date')
        total = data.count()
        data = Paginator(data, 12)
        page = request.GET.get('page')

        try:
            data = data.get_page(page)
        except PageNotAnInteger:
            data = data.page(1)
        except EmptyPage:
            data = data.page(data.num_pages)

        
        return render(request, 'users/admin_sites/pending_deposit_payments.html',
                      {'pending_sales': data, 'total': total})
    if request.user.is_staff and request.user.is_superuser:
        return render(request, 'users/admin_sites/pending_deposit_payments.html')
    return redirect('dashboard')