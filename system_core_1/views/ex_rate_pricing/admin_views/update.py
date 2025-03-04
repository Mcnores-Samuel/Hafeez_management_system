"""This module contains the admin site updates for cost_per_invoice and daily_exchange_rate."""
from django.utils import timezone
from system_core_1.models.cost_per_invoice import CostPerInvoice
from system_core_1.models.cost_per_invoice import DailyExchangeRate
from system_core_1.models.main_storage import MainStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt


@login_required
def update_cost_by_rate(request):
    """Update the cost per invoice by exchange rate."""
    if request.method == 'GET':
        invoices = CostPerInvoice.objects.filter(is_paid=False)
        exchange_rate = DailyExchangeRate.objects.filter(valid=True).first()

        if not exchange_rate:
            return JsonResponse({'error': 'No valid exchange rate found.'}, status=400)

        items_to_update = []
        invoices_to_update = []

        for invoice in invoices:
            for item in invoice.items.all():
                if item.in_stock and not item.sold:
                    if item.original_rate == 0:
                        item.original_rate = exchange_rate.exchange_rate
                    
                    item.cost_per_ex_rate = item.cost * exchange_rate.exchange_rate / item.original_rate
                    items_to_update.append(item)

        # Bulk update all items
        MainStorage.objects.bulk_update(items_to_update, ['original_rate', 'cost_per_ex_rate'])

        # Now update invoice cost_per_ex_rate after items are updated
        for invoice in invoices:
            invoice.cost_per_ex_rate = invoice.items.aggregate(total=Sum('cost_per_ex_rate'))['total'] or 0
            invoice.updated_at = timezone.now()
            invoices_to_update.append(invoice)

        # Bulk update invoices
        CostPerInvoice.objects.bulk_update(invoices_to_update, ['cost_per_ex_rate', 'updated_at'])

        return JsonResponse({'message': 'Cost per invoice updated successfully.'})

    return JsonResponse({'error': 'Invalid request.'}, status=400)


@login_required
@csrf_exempt
def invoice_paid(request, invoice_id):
    """Update the invoice as paid."""
    if request.method == 'POST':
        invoice = CostPerInvoice.objects.filter(id=invoice_id).first()

        if not invoice:
            return JsonResponse({'error': 'Invoice not found.'}, status=400)

        invoice.is_paid = True
        invoice.date_paid = timezone.now()
        invoice.updated_at = timezone.now()
        invoice.save()

        return JsonResponse({'message': 'Invoice paid successfully.'})

    return JsonResponse({'error': 'Invalid request.'}, status=400)
