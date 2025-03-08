"""This module contains the record airtel devices payment view."""
from ...models.promoter_payments import PromoterPayments
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ...models.user_profile import UserProfile
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt
def record_airtel_devices_payment(request):
    """This view records the payment made by a promoter for Airtel devices."""
    if request.user.is_superuser:
        if request.method == 'POST':
            promoter_id = request.POST.get('promoter_id')
            amount_paid = request.POST.get('Amount_paid', 0)
            payment_method = request.POST.get('payment_method', 'Cash')
            if not amount_paid:
                amount_paid = 0
            total_mifi_paid = request.POST.get('id_mifi', 0)
            if not total_mifi_paid:
                total_mifi_paid = 0
            total_idu_paid = request.POST.get('id_idu', 0)
            if not total_idu_paid:
                total_idu_paid = 0
            total_devices_paid = int(total_mifi_paid) + int(total_idu_paid)
            updated_by = request.user

            promoter = UserProfile.objects.get(id=promoter_id)

            PromoterPayments.objects.create(
                promoter=promoter,
                amount_paid=amount_paid,
                total_mifi_paid=total_mifi_paid,
                total_idu_paid=total_idu_paid,
                total_devices_paid=total_devices_paid,
                payment_date=timezone.now(),
                payment_method=payment_method,
                updated_by=updated_by
            )

            return redirect('airtel_device_data_entry')
    return redirect('dashboard')