"""This model represent the entire stock available and sold in all posts."""
from ....models.main_storage import MainStorage
from ....models.main_storage import Airtel_mifi_storage
from system_core_1.models.cost_per_invoice import CostPerInvoice
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from datetime import datetime
import json
from django.utils import timezone


def stockQuery(request):
    """Query the stock of phones available in the inventory."""
    if request.method == 'GET':
        # Get all devices in stock and assigned to agents in one query
        devices = MainStorage.objects.filter(
            in_stock=True,
            sold=False, missing=False, pending=False,
            agent__groups__name__in=['agents', 'branches']
            ).values_list('device_imei', flat=True)
        devices = reversed(devices)
        return JsonResponse({'data': list(devices)}, status=200)
    return JsonResponse({'message': 'Invalid request method'}, status=400)


def partners_stockQuery(request):
    """Query the stock of phones available in the inventory."""
    if request.method == 'GET':
        # Get all devices in stock and assigned to agents in one query
        invoices = CostPerInvoice.objects.filter(is_paid=False)
        data = []
        for invoice in invoices.all():
            items = invoice.items.all()
            for item in items:
                if item.in_stock:
                    data.append(item.device_imei)
        return JsonResponse({'data': data}, status=200)
    return JsonResponse({'message': 'Invalid request method'}, status=400)


def partner_invoices(request, partner_username):
    """Query the stock of phones available in the inventory."""
    if request.method == 'GET':
        # Get all devices in stock and assigned to agents in one query
        invoices = CostPerInvoice.objects.filter(
            is_paid=False,
            partner__username=partner_username
            )
        data = []
        for invoice in invoices:
            data.append({
                'invoice_number': invoice.invoice_number,
                'invoice_date': invoice.invoice_date,
                'items': list(invoice.get_invoice_items().values(
                    'device_imei', 'name', 'cost', 'in_stock', 'sold', 'collected_on',
                ))
            })
        return JsonResponse({'data': data}, status=200)
    return JsonResponse({'message': 'Invalid request method'}, status=400)


def pendingSales(request):
    """Query the sales of phones that are pending in the inventory."""
    if request.method == 'GET':
        # Get all devices in stock and assigned to agents in one query
        one_hr_ago = timezone.now() - timezone.timedelta(hours=1)
        devices = MainStorage.objects.filter(
            in_stock=False,
            sold=True,
            pending=True,
            recieved=True,
            missing=False
            ).values_list('device_imei', flat=True)
        devices = reversed(devices)
        return JsonResponse({'data': list(devices)}, status=200)
    return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
def updateTimeStamp(request):
    """Update the timestamp of a phone in the inventory."""
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            imei = data.get('imei')

            if imei is None:
                return JsonResponse({'message': 'Missing required fields'}, status=400)
            
            # Get the device and update it
            try:
                device = MainStorage.objects.get(device_imei=imei)
                device.last_updated = timezone.now()
                device.save()
                return JsonResponse({'message': 'Timestamp updated successfully'}, status=200)
            except MainStorage.DoesNotExist:
                return JsonResponse({'message': 'Device not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
def salesUpdates(request):
    """This function updates the sales of phones in the inventory."""
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            imei = data.get('imei')
            info = data.get('info')

            if imei is None or info is None:
                return JsonResponse({'message': 'Missing required fields'}, status=400)

            # Check if 'DEPLOYED' is in the info array
            status = 'DEPLOYED' in info

            # Extract the second timestamp from the info array
            date_pattern = r'\w{3} \d{1,2}, \d{4}, \d{1,2}:\d{2} (AM|PM)'
            timestamps = [item for item in info if re.match(date_pattern, item)]

            # Ensure there are at least two timestamps in the list
            if len(timestamps) >= 2:
                date_sold_str = timestamps[1]  # Get the second timestamp
            else:
                return JsonResponse({'message': 'Not enough valid timestamps found in info'}, status=400)

            # Extract and process prices
            prices = [item for item in info if re.match(r'MWK \d{1,3}(,\d{3})*', item)]
            numeric_prices = [int(price.replace('MWK ', '').replace(',', '')) for price in prices]
            numeric_prices.sort(reverse=True)

            price = 0

            if len(numeric_prices) >= 2:
                second_largest_price = numeric_prices[1]
                if second_largest_price > 0:
                    price = second_largest_price

            # Convert the date string to a Django date object
            date_sold_obj = datetime.strptime(date_sold_str, '%b %d, %Y, %I:%M %p')

            # Get the device and update it
            try:
                if status:
                    device = MainStorage.objects.get(device_imei=imei)
                    device.recieved = True
                    device.in_stock = False
                    device.sold = True
                    device.price = price
                    device.paid = True
                    device.pending = False
                    device.sales_type = "Loan"
                    device.stock_out_date = date_sold_obj
                    device.save()
                return JsonResponse({'message': 'Success'}, status=200)
            except MainStorage.DoesNotExist:
                return JsonResponse({'message': 'Device not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt
def airtel_sales_data(request):
    """Get the IDUs of the Airtel MiFi devices."""
    if request.method == 'GET':
        idus = Airtel_mifi_storage.objects.filter(
            in_stock=False,
            activated=True,
            data_submitted=False,
            paid=True,
            ).values_list('device_imei', 'device_type', 'device_phone_no')
        return JsonResponse({'data': list(idus)}, status=200)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            imei = data.get('imei')
            
            if imei is None:
                return JsonResponse({'message': 'Missing required fields'}, status=400)
            
            # Get the device and update it
            try:
                device = Airtel_mifi_storage.objects.get(device_imei=imei)
                device.data_submitted = True
                device.date_submitted = timezone.now()
                device.save()
                return JsonResponse({'message': 'Data submitted successfully'}, status=200)
            except Airtel_mifi_storage.DoesNotExist:
                return JsonResponse({'message': 'Device not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    return JsonResponse({'message': 'Invalid request method'}, status=400)