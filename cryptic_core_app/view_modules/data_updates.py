from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms import UserProfileForm
from ..models import AgentProfile, AgentStock, PhoneData, phone_reference
from django.http import JsonResponse

@login_required
def profile(request):
    user = request.user
    profile_form = None
    if request.method == 'POST':
        if 'first_name' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile information was successfully updated.')
                return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user)
    context = {
            'profile': user.email[0],
            'user': user,
            'profile_form': profile_form,
        }
    return render(request, 'users/profile.html', context)


@login_required
def change_password(request):
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
    
    return render(request, 'users/change_password.html', context)


@login_required
def in_stock(request):
    context = None
    if request.user.groups.filter(name='agents').exists():
        user = request.user
        agent_profile = AgentProfile.objects.get(user=user)
        stock_in = AgentStock.objects.filter(agent=agent_profile, in_stock=True)
        reference = phone_reference.objects.all()
        context = {
            'profile': user.email[0],
            'user': user,
            'stock_in': stock_in,
            'reference_list': reference
        }
    return render(request, 'users/in_stock.html', context)


@login_required
def stock_out(request):
    context = None
    if request.user.groups.filter(name='agents').exists():
        user = request.user
        agent_profile = AgentProfile.objects.get(user=user)
        stock_out = AgentStock.objects.filter(agent=agent_profile, in_stock=False)
        context = {
            'profile': user.email[0],
            'user': user,
            'stock_out': stock_out
        }
    return render(request, 'users/stock_out.html', context)


def add_contract_number(request):
    if request.method == 'POST':
        imei_number = request.POST.get('imei_number', None)
        contract_number = request.POST.get('contract_number', None)
        if contract_number and imei_number:
            agent_stock = AgentStock.objects.get(imei_number=imei_number, in_stock=False)
            phone_sold = PhoneData.objects.get(imei_number=imei_number)
            if agent_stock and phone_sold:
                agent_stock.contract_number = contract_number
                phone_sold.contract_number = contract_number
                agent_stock.save()
                phone_sold.save()
            return JsonResponse({'message': 'Data added successfully'})
    return render(request, 'users/agents.html')