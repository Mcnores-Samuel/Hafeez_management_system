from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms.user_profile_update_form import UserProfileForm
from ..forms.users import UserAvatarForm
from ..models.main_storage import MainStorage
from django.http import JsonResponse
from ..models.user_profile import UserAvatar
from ..data_query_engine.agents_queries.agents_data_query import AgentsDataQuery
from ..forms.filters import FilterAgentAndDataStockOut
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
    elif request.user.groups.filter(name='staff_members').exists():
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
        return render(request, 'users/staff_sites/profile.html', context)
    elif request.user.is_superuser:
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
        return render(request, 'users/admin_sites/profile.html', context)
    elif request.user.groups.filter(name='branches').exists():
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
        return render(request, 'users/branches/profile.html', context)
    elif request.user.groups.filter(name='MBOs').exists():
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
        return render(request, 'users/mbos/profile.html', context)
    return redirect('dashboard')


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
    total = 0
    user = request.user
    stock_in, total = AgentsDataQuery().stock(user=user, status=True, request=request)
    if request.method == 'POST':
        stock_in, total = AgentsDataQuery().search(
            user, request.POST.get('search_term', None),
            request, status=True, sold=False)
        
    context = {
        'stock_in': stock_in, 'total': total
    }
    if request.user.groups.filter(name='branches').exists():
        return render(request, 'users/branches/stock.html', context)
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
    total = 0
    month = request.GET.get('month', timezone.now().date().month)
    year = request.GET.get('year', timezone.now().date().year)
    stock_out, total = AgentsDataQuery().stock(user, False, request, month=month, year=year)
    form = FilterAgentAndDataStockOut(initial={'month': month, 'year': year})
    if request.method == 'POST':
        form = FilterAgentAndDataStockOut(request.POST)
        search_term = request.POST.get('search_term', None)
        if form.is_valid():
            month = form.cleaned_data.get('month', None)
            year = form.cleaned_data.get('year', None)
            stock_out, total = AgentsDataQuery().stock(user, False, request, month, year)
        elif search_term:
            stock_out, total = AgentsDataQuery().search_stock_out(
                user, search_term, request)
    context = {
        'sales': stock_out,
        'form': form,
        'total': total
    }
    if request.user.groups.filter(name='branches').exists():
        return render(request, 'users/branches/sales.html', context)
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
            if main_storage:
                main_storage.contract_no = contract_number
                main_storage.save()
                messages.success(request,
                                 'Contract No: {} for IMEI: {} added successfully'.format(
                                     contract_number, imei_number))
        if request.user.is_superuser:
            return redirect('pending_sales')
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
                    return redirect('new_stock')
    if request.method == 'GET':
        total = MainStorage.objects.filter(
            agent=request.user, recieved=False).count()
        return JsonResponse({'total': total})
    return redirect('new_stock')
    
