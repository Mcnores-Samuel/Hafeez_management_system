from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms.user_profile_update_form import UserProfileForm
from ..models.agent_profile import AgentProfile
from ..models.main_storage import MainStorage
from ..models.reference import Phone_reference
from ..models.customer_order import PhoneData
from django.http import JsonResponse
from ..forms.users import UserAvatarForm
from ..models.user_profile import UserAvatar

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
                                                  assigned=True).all()
            reference = Phone_reference.objects.all()
            context = {
                'profile': user.email[0],
                'user': user,
                'stock_in': stock_in,
                'reference_list': reference
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
    if request.user.groups.filter(name='agents').exists():
        user = request.user
        agent_profile = AgentProfile.objects.get(user=user)
        if agent_profile:
            stock_out = MainStorage.objects.filter(agent=user, in_stock=False,
                                                   assigned=True).all().order_by('-stock_out_date')
            context = {
                'profile': user.email[0],
                'user': user,
                'stock_out': stock_out,
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
        imei_number = request.POST.get('device_imei', None)
        contract_number = request.POST.get('contract_number', None)
        if contract_number and imei_number:
            main_storage = MainStorage.objects.get(device_imei=imei_number)
            phone_sold = PhoneData.objects.get(imei_number=imei_number)
            if main_storage and phone_sold:
                phone_sold.contract_number = contract_number
                main_storage.contract_no = contract_number
                phone_sold.save()
                main_storage.save()
            return JsonResponse({'message': 'Data added successfully'})
    return render(request, 'users/agent_sites/agents.html')

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
        imei_number = request.POST.get('device_imei', None)
        if imei_number:
            main_storage = MainStorage.objects.get(device_imei=imei_number)
            if main_storage:
                main_storage.recieved = True
                main_storage.save()
            return JsonResponse({'message': 'verified successfully'})
        else:
            return JsonResponse({'message': 'Error verifying stock'})
    return render(request, 'users/agent_sites/agents.html')
