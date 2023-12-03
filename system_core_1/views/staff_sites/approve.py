from ...models.customer_details import CustomerData
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


def approve(request):
    """This view marks a customer as approved."""
    if request.user.groups.filter(name='staff_members').exists():
        if request.method == 'GET':
            current_week = timezone.now().date()
            monday = current_week - timezone.timedelta(days=current_week.weekday())
            sunday = monday + timezone.timedelta(days=6)
            customers = CustomerData.objects.filter(
                created_at__range=[monday, sunday],
                approved=False, read=True, rejected=False).order_by('-created_at')
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
    return render(request, 'users/staff_sites/approve.html', context)


def get_total_to_approve(request):
    """This view returns the total number of
    customers to be approved in the current week.
    """
    if request.user.groups.filter(name='staff_members').exists():
        if request.method == 'GET':
            current_week = timezone.now().date()
            monday = current_week - timezone.timedelta(days=current_week.weekday())
            sunday = monday + timezone.timedelta(days=6)
            total_to_approve = CustomerData.objects.filter(
            created_at__range=[monday, sunday],
            approved=False, pending=True, rejected=False, read=True).order_by('-created_at').count()
            return JsonResponse({'total_to_approve': total_to_approve})
    return JsonResponse({'error': 'something went wrong'})


@login_required
def approved(request):
    """This view returns the total number of
    approved customers in the current week.
    """
    if request.user.groups.filter(name='staff_members').exists():
        if request.method == 'GET':
            current_week = timezone.now().date()
            monday = current_week - timezone.timedelta(days=current_week.weekday())
            sunday = monday + timezone.timedelta(days=6)
            total_approved = CustomerData.objects.filter(
            created_at__range=[monday, sunday],
            approved=True).order_by('-created_at').count()
            return JsonResponse({'total_approved': total_approved})
    return JsonResponse({'error': 'something went wrong'})


def get_approved_data(request):
    """This view returns the total number of approved customers in the current week."""
    if request.user.groups.filter(name='staff_members').exists():
        if request.method == 'GET':
            current_week = timezone.now().date()
            monday = current_week - timezone.timedelta(days=current_week.weekday())
            sunday = monday + timezone.timedelta(days=6)
            customers = CustomerData.objects.filter(
                created_at__range=[monday, sunday], approved=True).order_by('-created_at')
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
    return render(request, 'users/staff_sites/approved.html', context)
