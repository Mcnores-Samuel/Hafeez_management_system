#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the home_page view function, which is the main entry point
for unauthenticated users into the application.
"""
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from ..forms.sign_in_form import SignInForm
from django_email_verification import verify_view, verify_token
from django.http import HttpResponse
from ..models.user_profile import UserAvatar
from django.contrib import messages
from ..models.main_storage import MainStorage
from ..models.agent_profile import AgentProfile
from ..forms.filters import FilterAgentAndData
from django.contrib.auth.models import Group
from ..models.user_profile import UserProfile


def home_page(request):
    """The `home_page` view function is the main entry point for unauthenticated users
    into the application.

    Functionality:
    - Checks if the user is authenticated.
    - Renders the home page, providing access to various application features.
    - May include different views, options, and functionalities based on user roles.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the application's home page.
    - Redirects authenticated users to the dashboard.

    Usage:
    - Unauthenticated users access this view to interact with the application's core
      functionalities.
    - Customizes the home page interface based on user roles and permissions.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        messages.success(request, f'Welcome {user.username}!!')
                        return redirect(reverse('dashboard'))
                    elif user.groups.filter(name='agents').exists():
                        messages.success(request, f'Welcome {user.username}!!')
                        return redirect(reverse('dashboard'))
                    else:
                        messages.success(request, f'Welcome {user.username}!!')
                        return redirect(reverse('dashboard'))
                else:
                    messages.error(request, 'Your account is not active')
            else:
                messages.error(request, 'Invalid login credentials')
    else:
        form = SignInForm()

    context = {'form': form}
    if request.user.is_authenticated:
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        context['avatar'] = avatar
        context['profile'] = request.user.email[0]
        return redirect(reverse('dashboard'))
    return render(request, 'base.html', context)


@verify_view
def confirm(request, token):
    """The `confirm` view function is responsible for handling the confirmation of
    user accounts.
    """
    success, user = verify_token(token)
    return HttpResponse(f'Account verified, {user.username}' if success else 'Invalid token')


def main_shop_details(request):
    """The `main_storage` view function is responsible for handling the display of the
    application's main_storage page.
    """
    if request.method == 'GET':
        form = FilterAgentAndData(request.GET)
        if form.is_valid():
            user = form.cleaned_data['user']
            stock = {}
            data_set = MainStorage.objects.filter(
                agent=user.user, in_stock=True, sold=False, assigned=True).order_by('id')
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1

            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
            context = {'stock': stock, 'user': user.user.username, 'form': form}
            return render(request, 'users/admin_sites/main_stock_details.html', context)
        else:
            form = FilterAgentAndData()
            main_shop_staff = Group.objects.get(name='main_shop')
            representatives = UserProfile.objects.filter(groups=main_shop_staff)
            data_set = MainStorage.objects.filter(
                agent__in=representatives,
                in_stock=True, sold=False,
                missing=False, assigned=True)
            stock = {}
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
    context = {'form': form, 'stock': stock, 'user': representatives[0].username}
    return render(request, 'users/admin_sites/main_stock_details.html', context)