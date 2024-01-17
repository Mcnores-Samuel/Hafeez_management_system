from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms.user_profile_update_form import UserProfileForm
from ..forms.users import UserAvatarForm
from ..models.main_storage import MainStorage, Airtel_mifi_storage
from ..models.customer_order import PhoneData
from django.http import JsonResponse
from ..models.user_profile import UserAvatar
from ..models.customer_details import CustomerData
from ..data_query_engine.agents_queries.agents_data_query import AgentsDataQuery
from django.db import IntegrityError


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
    avatar_form = None
    if request.user.groups.filter(name='agents').exists():
        if request.method == 'POST':
            profile_form = UserProfileForm(request.POST, user=request.user)
            if profile_form.is_valid():
                profile = profile_form.process_profile()
                if profile:
                    messages.success(request, 'Your profile information was successfully updated.')
                    return redirect('profile')
                else:
                    messages.error(request, 'An error occurred while updating your profile information.')
                    return redirect('profile')
        else:
            profile_form = UserProfileForm(user=request.user)
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        context = {
                'profile': user.email[0],
                'user': user,
                'form': profile_form,
                'avatar': avatar
            }
        return render(request, 'users/agent_sites/profile.html', context)
    return render(request, 'users/general-sites/profile.html', context)

@login_required
def upload_image(request):
    """Uploads the user's profile image.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        avatar_form = UserAvatarForm(request.POST, request.FILES)
        if avatar_form.is_valid():
            # Get or create UserAvatar instance for the current user
            avatar, created = UserAvatar.objects.get_or_create(user=request.user)
            
            if not created and avatar.image:
                avatar.image.delete()
            avatar.image = avatar_form.cleaned_data['image']
            avatar.save()
            messages.success(request, 'Your profile picture was successfully updated.')
            return redirect('profile')

    return redirect('profile')


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
    user = request.user
    stock_in = AgentsDataQuery().stock(user, True, request)
    if request.method == 'POST':
        stock_in = AgentsDataQuery().search(
            user, request.POST.get('search_term', None),
            request, status=True, sold=False)
    context = {
        'stock_in': stock_in
    }
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
    user = request.user
    stock_out = AgentsDataQuery().stock(user, False, request)
    if request.method == 'POST':
        stock_out = AgentsDataQuery().search_stock_out(
            user, request.POST.get('search_term', None),
            request)
    context = {
        'sales': stock_out
    }
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
