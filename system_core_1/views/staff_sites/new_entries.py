from ...models.customer_details import CustomerData
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib import messages


@login_required
def get_new_entries_total(request):
    """This view returns the total number of new entries
    in the current week.
    """
    if request.user.groups.filter(name='staff_members').exists():
        if request.method == 'GET':
            current_week = timezone.now().date()
            monday = current_week - timezone.timedelta(days=current_week.weekday())
            sunday = monday + timezone.timedelta(days=6)
            total_new_entries = CustomerData.objects.filter(
            created_at__range=[monday, sunday],
            approved=False, pending=True, rejected=False, read=False).order_by('-created_at').count()
            return JsonResponse({'total_new_entries': total_new_entries})
    return JsonResponse({'error': 'something went wrong'})


@login_required
def get_new_entries(request):
    """This view returns the total number of new entries
    in the current week.
    """
    if request.user.groups.filter(name='staff_members').exists():
        if request.method == 'GET':
            current_week = timezone.now().date()
            monday = current_week - timezone.timedelta(days=current_week.weekday())
            sunday = monday + timezone.timedelta(days=6)
            customers = CustomerData.objects.filter(
                created_at__range=[monday, sunday], approved=False,
                pending=True, rejected=False, read=False).order_by('-created_at')
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
    return render(request, 'users/staff_sites/new_entries.html', context)


def mark_as_read(request):
    """This view marks a customer as read."""
    if request.user.groups.filter(name='staff_members').exists():
        if request.method == 'POST':
            customer_id = request.POST.get('customer_id', None)
            customer = CustomerData.objects.get(id=customer_id)
            customer.read = True
            customer.save()
            messages.success(request, 'customer marked as read')
            return redirect('get_new_entries')
    messages.error(request, 'something went wrong')
    return redirect('get_new_entries')
    