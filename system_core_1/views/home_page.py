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
from ..models.user_profile import UserProfile
from system_core_1.models.cost_per_invoice import CostPerInvoice
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from webpush import send_user_notification
import json


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
    return redirect(reverse('sign_in'))


@verify_view
def confirm(request, token):
    """The `confirm` view function is responsible for handling the confirmation of
    user accounts.
    """
    success, user = verify_token(token)
    return HttpResponse(f'Account verified, {user.username}' if success else 'Invalid token')

