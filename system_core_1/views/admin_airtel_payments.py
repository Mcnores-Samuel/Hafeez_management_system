"""This view function is responsible for payments updates in the Airtel system."""
from ..models.promoter_payments import PromoterPayments
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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
                'updated_by': payment.updated_by.username,
                'seen': payment.seen
            })
        return JsonResponse({'total': total, 'data': data})
    return redirect('dashboard')