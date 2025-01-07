"""This module contains the views related to the stock taking."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..models.main_storage import MainStorage
from django.contrib import messages as message
from django.http import JsonResponse
import json


@login_required
@csrf_exempt
def stock_taking(request):
    if request.method == 'POST' and request.user.is_superuser:
        data = request.POST.get('data', None)
        if data:
            scanned_items = json.loads(data)
            not_in_stock = []
            for imei in scanned_items:
                try:
                    device = MainStorage.objects.get(device_imei=imei, in_stock=True)
                    device.available = True
                    device.save()
                except MainStorage.DoesNotExist:
                    not_in_stock.append(imei)
            return JsonResponse({'status': 200, 'not_in_stock': not_in_stock})
        return JsonResponse({'status': 400, 'message': 'Invalid request data format'})
    if request.user.is_superuser:
        return render(request, 'users/admin_sites/stock_taking.html')
    return redirect('dashboard')
