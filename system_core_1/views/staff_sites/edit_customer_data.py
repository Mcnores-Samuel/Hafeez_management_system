from ...models.customer_details import CustomerData
from ...forms.update_customer_data import CustomerDataForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


@login_required
def edit_customer_data(request, customer_id):
    """This view edits customer data in the current week.
    The view is only accessible to staff members and
    is used to edit customer data.
    """
    context = {}
    if request.user.groups.filter(name='staff_members').exists():
        form = None
        if request.method == 'POST':
            customer = CustomerData.objects.get(id=customer_id)
            form = CustomerDataForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                messages.success(request, 'Customer data updated successfully')
                return redirect('approve')
            else:
                messages.error(request, 'Something went wrong')
                # Creating form with instance for the context
                form = CustomerDataForm(instance=customer)
        else:
            customer = CustomerData.objects.get(id=customer_id)
            form = CustomerDataForm(instance=customer)
            
        context = {
            'form': form,
            'customer_id': customer_id,
        }
    return render(request, 'users/staff_sites/edit_customer_data.html', context)
