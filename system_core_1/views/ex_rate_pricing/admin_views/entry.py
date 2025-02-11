"""This module contains the views for the ex_rate_pricing app."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from system_core_1.models.cost_per_invoice import CostPerInvoice
from system_core_1.models.cost_per_invoice import DailyExchangeRate
from system_core_1.models.user_profile import UserProfile
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages



@login_required
def ex_rate_pricing(request):
    """Display the exchange rate pricing page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    partners = UserProfile.objects.filter(groups__name='partners')
    return render(request, 'users/admin_sites/ex_rate_pricing.html', {'partners': partners})


@login_required
@csrf_exempt
def data_per_partner(request):
    """Returns data for the requested partner with optimized queries."""
    if request.method == 'POST':
        partner_id = request.POST.get('partner')

        # Get partner safely without exceptions
        partner = UserProfile.objects.filter(groups__name='partners', id=partner_id).first()

        # Optimize invoice query using select_related & prefetch_related
        invoices = CostPerInvoice.objects.filter(
            partner=partner, is_paid=False
        ).select_related('partner').prefetch_related('items')

        # Fetch only required fields
        invoices_data = []
        for invoice in invoices:
            invoice_data = {
                'invoice_number': invoice.invoice_number,
                'invoice_date': invoice.invoice_date,
                'total_invoice_items': invoice.total_invoice_items,
                'original_cost': invoice.original_cost,
                'cost_per_ex_rate': invoice.cost_per_ex_rate,
                'total_items_sold': invoice.total_items_sold,
                'is_paid': invoice.is_paid,
                'date_paid': invoice.date_paid,
                'last_payment_amount': invoice.last_payment_amount,
                'last_payment_date': invoice.last_payment_date,
                'last_payment_method': invoice.last_payment_method,
                'current_balance': invoice.current_balance,
                'total_amount_paid': invoice.total_amount_paid,
                # Convert get_invoice_items() queryset to list of dicts
                'items': list(invoice.get_invoice_items().values(
                    'device_imei', 'name', 'cost', 'price', 'in_stock', 'sold', 'pending',
                    'stock_out_date', 'collected_on', 'cost_per_ex_rate'
                ))
            }
            invoices_data.append(invoice_data)

        return JsonResponse({'invoices': invoices_data}, safe=False)

    return JsonResponse({'error': 'Invalid request.'}, status=400)


@login_required
@csrf_exempt
def add_exchange_rate(request):
    """Add a new exchange rate to the system."""
    if request.method == 'POST':
        exchange_rate = request.POST.get('current_ex_rate')
        # Validate exchange rate and date
        exchange_rate = float(exchange_rate)
        previous_rate = DailyExchangeRate.objects.filter(valid=True).first()
        if previous_rate:
            previous_rate.valid = False
            previous_rate.save()
        date = timezone.now()
        if exchange_rate:
            ex_rate = DailyExchangeRate.objects.create(
                exchange_rate=exchange_rate,
                date=date, valid=True
            )
            res = {
                'current_ex_rate': ex_rate.exchange_rate,
                'message': 'Exchange rate added successfully.'
            }
            return JsonResponse(res)
        else:
            return JsonResponse({'error': 'Invalid exchange rate.'}, status=400)
    return JsonResponse({'error': 'Invalid request.'}, status=400)


@login_required
def get_exchange_rate(request):
    """Get the current exchange rate."""
    if request.method == 'GET':
        exchange_rate = DailyExchangeRate.objects.filter(valid=True).first()
        if exchange_rate:
            return JsonResponse({'current_ex_rate': exchange_rate.exchange_rate})
    return JsonResponse({'error': 'No exchange rate found.'}, status=404)


@login_required
def get_outstanding_invoice(request):
    """Get the total outstanding invoice for the month."""
    if request.method == 'GET':
        invoices = CostPerInvoice.objects.filter(is_paid=False)
        total_outstanding = invoices.count()
        return JsonResponse({'total_outstanding': total_outstanding})
    return JsonResponse({'error': 'No outstanding invoice found.'}, status=404)