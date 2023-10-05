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
                        return redirect(reverse('home_page'))
                    elif user.groups.filter(name='agents').exists():
                        return redirect(reverse('home_page'))
                    else:
                        return redirect(reverse('home_page'))
                else:
                    form.add_error(None, "Please!! activate your account")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = SignInForm()
    context = {'form': form}
    if request.user.is_authenticated:
        context['profile'] = request.user.email[0]
    return render(request, 'base.html', context)

@verify_view
def confirm(request, token):
    """The `confirm` view function is responsible for handling the confirmation of
    user accounts.
    """
    success, user = verify_token(token)
    return HttpResponse(f'Account verified, {user.username}' if success else 'Invalid token')
