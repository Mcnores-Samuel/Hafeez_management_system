"""This view function is responsible for payments updates in the Airtel system."""
from ..models.promoter_payments import PromoterPayments
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages


@login_required
def currentPayments(request):
    """Display the current payments data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
        Returns a list of current payments to be resolved.
    """
    if request.user.is_superuser and request.method == 'GET':
        payments = PromoterPayments.objects.filter(
            seen=False, updated_completed=False).order_by('-payment_date')
        
        total = payments.count()
        data = []

        for payment in payments:
            data.append({
                'id': payment.id,
                'promoter': payment.promoter.first_name + ' ' + payment.promoter.last_name,
                'amount_paid': payment.amount_paid,
                'total_mifi_paid': payment.total_mifi_paid,
                'total_idu_paid': payment.total_idu_paid,
                'total_devices_paid': payment.total_devices_paid,
                'payment_date': payment.payment_date,
                'validity': payment.valid,
                'payment_method': payment.payment_method,
                'updated_by': payment.updated_by.username,
                'seen': payment.seen
            })
        return JsonResponse({'total': total, 'data': data})
    return redirect('dashboard')


def concludedPayments(request):
    """Display the concluded payments data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
        Returns a list of concluded payments.
    """
    if request.user.is_superuser and request.method == 'GET':
        payments = PromoterPayments.objects.filter(
            updated_completed=True).order_by('-payment_date')
        
        total = payments.count()
        data = []

        for payment in payments:
            data.append({
                'id': payment.id,
                'promoter': payment.promoter.first_name + ' ' + payment.promoter.last_name,
                'amount_paid': payment.amount_paid,
                'total_mifi_paid': payment.total_mifi_paid,
                'total_idu_paid': payment.total_idu_paid,
                'total_devices_paid': payment.total_devices_paid,
                'payment_date': payment.payment_date,
                'validity': payment.valid,
                'payment_method': payment.payment_method,
                'updated_by': payment.updated_by.username,
                'seen': payment.seen
            })
        return JsonResponse({'total': total, 'data': data})
    return redirect('dashboard')


@login_required
@csrf_exempt
def renewPayment(request):
    """Renew the payment data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
        Returns a list of renewed payments.
    """
    if request.user.is_superuser and request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        payment = PromoterPayments.objects.get(id=payment_id)
        payment.seen = False
        payment.payment_date = timezone.now()
        payment.save()
        messages.success(request, 'Payment renewed successfully.')
        return redirect('airtel_device_data_entry')
    messages.error(request, 'An error occurred. Please try again.')
    return redirect('airtel_device_data_entry')


@login_required
@csrf_exempt
def deletePayment(request):
    """Delete the payment data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
        Returns a list of deleted payments.
    """
    if request.user.is_superuser and request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        payment = PromoterPayments.objects.get(id=payment_id)
        payment.delete()
        messages.success(request, 'Payment deleted successfully.')
        return redirect('airtel_device_data_entry')
    messages.error(request, 'An error occurred. Please try again.')
    return redirect('airtel_device_data_entry')