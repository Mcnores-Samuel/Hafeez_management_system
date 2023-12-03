from ...models.customer_details import CustomerData
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib import messages


def total_rejected(request):
    """This view returns the total number of rejected entries
    in the current week.
    """
    if request.user.groups.filter(name='staff_members').exists():
        if request.method == 'GET':
            current_week = timezone.now().date()
            monday = current_week - timezone.timedelta(days=current_week.weekday())
            sunday = monday + timezone.timedelta(days=6)
            total_rejected = CustomerData.objects.filter(
                created_at__range=[monday, sunday],
                approved=False, pending=False, rejected=True, read=True).order_by('-created_at').count()
            return JsonResponse({'total_rejected': total_rejected})
    return JsonResponse({'error': 'something went wrong'})

@login_required
def get_rejected(request):
    """This view returns the total number of rejected entries
    in the current week.
    """
    if request.user.groups.filter(name='staff_members').exists():
        if request.method == 'GET':
            current_week = timezone.now().date()
            monday = current_week - timezone.timedelta(days=current_week.weekday())
            sunday = monday + timezone.timedelta(days=6)
            customers = CustomerData.objects.filter(
                created_at__range=[monday, sunday], approved=False,
                pending=False, rejected=True, read=True).order_by('-created_at')
            customers = [(customer, list(customer.phonedata_set.all())) for customer in customers]

            paginator = Paginator(customers, 6)
            page_number = request.GET.get('page')
            
            try:
                customers = paginator.page(page_number)
            except PageNotAnInteger:
                customers = paginator.page(1)
            except EmptyPage:
                customers = paginator.page(paginator.num_pages)

            context = {
                'customers': customers
            }
    return render(request, 'users/staff_sites/rejected.html', context)