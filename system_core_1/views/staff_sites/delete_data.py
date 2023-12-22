from ...models.customer_details import CustomerData
from ...models.main_storage import MainStorage
from django.contrib import messages
from django.shortcuts import redirect


def delete_customer_data(request):
    """The `delete_customer_data` function is responsible for deleting a customer's
    data.
    """
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id', None)
        if customer_id:
            customer = CustomerData.objects.get(id=customer_id)
            device = MainStorage.objects.get(
                device_imei=customer.phonedata_set.all()[0].imei_number)
            device.sold = False
            device.in_stock = True
            device.sales_type = '##'
            device.save()
            customer.delete()
        messages.success(request, 'Customer data deleted successfully')
        return redirect('dashboard')
    messages.error(request, 'Something went wrong')
    return redirect('dashboard')