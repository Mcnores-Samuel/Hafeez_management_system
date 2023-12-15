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
from ..models.main_storage import MainStorage
from ..models.reference import Phone_reference
from ..models.user_profile import UserAvatar


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
                        return redirect(reverse('dashboard'))
                    elif user.groups.filter(name='agents').exists():
                        return redirect(reverse('dashboard'))
                    else:
                        return redirect(reverse('dashboard'))
                else:
                    form.add_error(None, "Please!! activate your account")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = SignInForm()
    products = {}
    itel = MainStorage.objects.filter(in_stock=True,
                                      category="Itel", sold=False).order_by('id')
    tecno = MainStorage.objects.filter(in_stock=True,
                                       category="Tecno", sold=False).order_by('id')
    infinix = MainStorage.objects.filter(in_stock=True,
                                         category="Infinix", sold=False).order_by('id')
    redmi = MainStorage.objects.filter(in_stock=True,
                                       category="Redmi", sold=False).order_by('id')
    skip = ['it2163', 'it5607', 'it5606', 'it2160', 'it2171', 'it2172']
    phone_list = []
    count = 0
    unique_phone_types = set()
    for phone in itel:
        if phone.phone_type not in unique_phone_types and phone.phone_type not in skip:
            phone_list.append(phone)
            unique_phone_types.add(phone.phone_type)
            count += 1
        if count == 6:
            break
    products['itel'] = phone_list
    unique_phone_types.clear()

    phone_list = []
    count = 0
    unique_phone_types = set()
    for phone in tecno:
        if phone.phone_type not in unique_phone_types:
            phone_list.append(phone)
            unique_phone_types.add(phone.phone_type)
            count += 1
        if count == 6:
            break
    products['tecno'] = phone_list
    unique_phone_types.clear()

    phone_list = []
    count = 0
    unique_phone_types = set()
    for phone in infinix:
        if phone.phone_type not in unique_phone_types:
            phone_list.append(phone)
            unique_phone_types.add(phone.phone_type)
            count += 1
        if count == 6:
            break
    products['infinix'] = phone_list
    unique_phone_types.clear()

    phone_list = []
    count = 0
    unique_phone_types = set()
    for phone in redmi:
        if phone.phone_type not in unique_phone_types:
            phone_list.append(phone)
            unique_phone_types.add(phone.phone_type)
            count += 1
        if count == 6:
            break
    products['redmi'] = phone_list
    unique_phone_types.clear()
    prices = Phone_reference.objects.all()
    context = {'form': form, 'products': products, 'prices': prices}
    if request.user.is_authenticated:
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        context['avatar'] = avatar
        context['profile'] = request.user.email[0]
    return render(request, 'base.html', context)


@verify_view
def confirm(request, token):
    """The `confirm` view function is responsible for handling the confirmation of
    user accounts.
    """
    success, user = verify_token(token)
    return HttpResponse(f'Account verified, {user.username}' if success else 'Invalid token')


def products(request, data_id=None):
    """The `products` view function is responsible for handling the display of the
    application's products page.
    """
    return render(request, 'users/general-sites/products.html')


def about(request):
    """The `about` view function is responsible for handling the display of the
    application's about page.
    """
    return render(request, 'users/general-sites/about.html')


def contact(request):
    """The `contact` view function is responsible for handling the display of the
    application's contact page.
    """
    return render(request, 'users/general-sites/contact.html')


def services(request):
    """The `services` view function is responsible for handling the display of the
    application's services page.
    """
    return render(request, 'users/general-sites/services.html')


def faq(request):
    """The `faq` view function is responsible for handling the display of the
    application's faq page.
    """
    return render(request, 'users/general-sites/faq.html')


def terms(request):
    """The `terms` view function is responsible for handling the display of the
    application's terms page.
    """
    return render(request, 'users/general-sites/terms.html')


def privacy(request):
    """The `privacy` view function is responsible for handling the display of the
    application's privacy page.
    """
    return render(request, 'users/general-sites/privacy.html')

def main_shop_details(request):
    """The `main_storage` view function is responsible for handling the display of the
    application's main_storage page.
    """
    return render(request, 'users/admin_sites/main_stock_details.html')