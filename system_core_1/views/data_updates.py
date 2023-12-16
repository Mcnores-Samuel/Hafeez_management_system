from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms.user_profile_update_form import UserProfileForm
from ..models.agent_profile import AgentProfile
from ..models.main_storage import MainStorage, Airtel_mifi_storage
from ..models.reference import Price_reference
from ..models.customer_order import PhoneData
from django.http import JsonResponse
from ..models.user_profile import UserAvatar
from ..models.customer_details import CustomerData
from django.utils import timezone


@login_required
def profile(request):
    """Display the user's profile.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    user = request.user
    profile_form = None
    if request.method == 'POST' and 'first_name' in request.POST:
        profile_form = UserProfileForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile information was successfully updated.')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user)
    avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
    context = {
            'profile': user.email[0],
            'user': user,
            'profile_form': profile_form,
            'avatar': avatar
        }
    return render(request, 'users/general-sites/profile.html', context)


@login_required
def change_password(request):
    """Change the user's password.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    user = request.user
    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(user)
    
    context = {
        'profile': user.email[0],
        'password_form': password_form,
    }
    
    return render(request, 'users/general-sites/change_password.html', context)


@login_required
def in_stock(request):
    """Checks agent's stock and displays the phones in stock.

    Args:
        request (HttpRequest): The request object.
    
    Returns:
        HttpResponse: The response object.
    """
    context = None
    if request.user.groups.filter(name='agents').exists():
        user = request.user
        agent_profile = AgentProfile.objects.get(user=user)
        if agent_profile:
            stock_in = MainStorage.objects.filter(agent=user, in_stock=True,
                                                  assigned=True).all().order_by('-entry_date')
            reference = Price_reference.objects.all()
            context = {
                'profile': user.email[0],
                'user': user,
                'stock_in': stock_in,
                'reference_list': reference
            }
    elif request.user.groups.filter(name='airtel_agents').exists():
        stock_in = Airtel_mifi_storage.objects.filter(agent=request.user,
                                                     in_stock=True,
                                                     assigned=True).all().order_by('-entry_date') 
        context = {
            'profile': request.user.email[0],
            'user': request.user,
            'stock_in': stock_in,
        }
        return render(request, 'users/airtel_agents/in_stock.html', context)
    return render(request, 'users/agent_sites/in_stock.html', context)


@login_required
def stock_out(request):
    """Checks agent's stock and displays the phones out of stock.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    context = None
    if request.user.groups.filter(name='agents').exists():
        user = request.user
        agent_profile = AgentProfile.objects.get(user=user)
        if agent_profile:
            current_month = timezone.now().date().month
            current_year = timezone.now().date().year
            stock_out = MainStorage.objects.filter(agent=user, in_stock=False,
                                                   assigned=True,
                                                   stock_out_date__month=current_month,
                                                   stock_out_date__year=current_year).order_by('-stock_out_date')
            context = {
                'profile': user.email[0],
                'user': user,
                'stock_out': stock_out,
            }
    elif request.user.groups.filter(name='airtel_agents').exists():
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        stock_out = Airtel_mifi_storage.objects.filter(agent=request.user,
                                                      in_stock=False, assigned=True,
                                                      stock_out_date__month=current_month,
                                                      stock_out_date__year=current_year).order_by('-stock_out_date')
        context = {
            'profile': request.user.email[0],
            'user': request.user,
            'stock_out': stock_out,
        }
        return render(request, 'users/airtel_agents/stock_out.html', context)
    return render(request, 'users/agent_sites/stock_out.html', context)


@login_required
def add_contract_number(request):
    """Adds contract number to the phone sold.
    user must be an agent to access this view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        imei_number = request.POST.get('imei_number', None)
        contract_number = request.POST.get('contract_number', None)
        if contract_number and imei_number:
            main_storage = MainStorage.objects.get(device_imei=imei_number)
            phone_sold = PhoneData.objects.get(imei_number=imei_number)
            if main_storage and phone_sold:
                phone_sold.contract_number = contract_number
                main_storage.contract_no = contract_number
                phone_sold.save()
                main_storage.save()
                messages.success(request, 'contract number added successfully')
    return redirect('dashboard')


@login_required
def verify_stock_recieved(request):
    """Verifies the stock recieved by the agent.
    user must be an agent to access this view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        if request.user.groups.filter(name='agents').exists():
            imei_number = request.POST.get('device_imei', None)
            if imei_number:
                main_storage = MainStorage.objects.get(device_imei=imei_number)
                if main_storage:
                    main_storage.recieved = True
                    main_storage.save()
                return JsonResponse({'message': 'verified successfully'})
            else:
                return JsonResponse({'message': 'imei number not found'})
            
        elif request.user.groups.filter(name='airtel_agents').exists():
            imei_number = request.POST.get('device_imei', None)
            if imei_number:
                main_storage = Airtel_mifi_storage.objects.get(device_imei=imei_number)
                if main_storage:
                    main_storage.recieved = True
                    main_storage.save()
                return JsonResponse({'message': 'verified successfully'})
            else:
                return JsonResponse({'message': 'imei number not found'})
    return redirect('dashboard')


@login_required
def update_customer_data(request):
    """Updates customer data.
    user must be an agent to access this view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        account_name = request.POST.get('account_name', None)
        customer_id = request.POST.get('customer_id', None)
        customer = CustomerData.objects.get(id=customer_id)
        if customer:
            customer.account_name = account_name
            customer.save()
            messages.success(request, 'customer data updated successfully')
    return redirect('dashboard')
