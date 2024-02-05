#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module contains the views for the application."""
from django.shortcuts import render
from ..forms import *
from django.contrib.auth.decorators import login_required
from ..models.agent_profile import AgentProfile
from ..models.user_profile import UserProfile
from ..models.main_storage import MainStorage
from ..forms.filters import FilterMainStorege
from ..forms.filters import FilterAgentAndData, FilterAgentAndDataSales
from ..models.user_profile import UserAvatar
from .search_and_filters import search
from django.contrib.auth.models import Group
from django.utils import timezone
from ..data_analysis_engine.admin_panel.calc_commitions import CalcCommissions


@login_required
def main_stock_details(request):
    """The `main_storage` view function is responsible for handling the display of the
    application's main_storage page.
    """
    if request.method == 'GET' and request.user.is_staff:
        form = FilterAgentAndData(request.GET)
        if form.is_valid():
            user = form.cleaned_data['user']
            stock = {}
            data_set = MainStorage.objects.filter(
                agent=user.user, in_stock=True, sold=False, assigned=True).order_by('id')
            total = data_set.count()
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1

            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
            context = {'stock': stock, 'user': user.user.username, 'form': form, 'total': total}
            return render(request, 'users/admin_sites/main_stock_details.html', context)
        else:
            form = FilterAgentAndData()
            main_shop_staff = Group.objects.get(name='main_shop')
            representatives = UserProfile.objects.filter(groups=main_shop_staff)
            data_set = MainStorage.objects.filter(
                agent__in=representatives,
                in_stock=True, sold=False,
                missing=False, assigned=True)
            total = data_set.count()
            stock = {}
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
    context = {'form': form, 'stock': stock, 'user': representatives[0].username, 'total': total}
    return render(request, 'users/admin_sites/main_stock_details.html', context)


@login_required
def main_sales_details(request):
    """The `main_storage` view function is responsible for handling the display of the
    application's main_storage page.

    Functionality:
        - Checks if the user is authenticated and is a staff member. Only staff members
            are allowed to access this view.
        - Renders the main storage page, displaying all phones in the main storage.
        - Implements search and filtering functionality.

    Note:
        This view assumes user authentication and validation of staff status have been
        handled in the authentication system and UserProfile model.
    """
    if request.method == 'GET' and request.user.is_staff:
        form = FilterAgentAndDataSales(request.GET)
        if form.is_valid():
            user = form.cleaned_data['user']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            stock = {}
            data_set = MainStorage.objects.filter(
                agent=user.user, in_stock=False, sold=True,
                assigned=True, pending=False, missing=False,
                stock_out_date__month=month, stock_out_date__year=year).order_by('id')
            total = data_set.count()
            CalcCommissions().update_commission(
                user.user, total,
                month=month, year=year)
            progress, target = CalcCommissions().target_progress(
                user.user, month=month, year=year)
            commision = CalcCommissions().calc_commission(
                user.user, month=month, year=year)
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1

            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
            context = {'stock': stock, 'user': user.user.username,
                       'form': form, 'total': total,
                       'progress': progress, 'target': target,
                       'commission': commision,}
            return render(request, 'users/admin_sites/main_sales_details.html', context)
        else:
            form = FilterAgentAndDataSales()
            main_shop_staff = Group.objects.get(name='main_shop')
            representatives = UserProfile.objects.filter(groups=main_shop_staff)
            year = timezone.now().date().year
            month = timezone.now().date().month
            data_set = MainStorage.objects.filter(
                agent__in=representatives,
                in_stock=False, sold=True,
                missing=False, assigned=True, pending=False,
                stock_out_date__month=month, stock_out_date__year=year)
            total = data_set.count()
            CalcCommissions().update_commission(
            representatives[0], total,
            month=timezone.now().date().month,
            year=timezone.now().date().year)
            progress, target = CalcCommissions().target_progress(representatives[0])
            stock = {}
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
    context = {'form': form, 'stock': stock,
               'user': representatives[0].username,
               'total': total, 'progress': progress,
               'target': target}
    return render(request, 'users/admin_sites/main_sales_details.html', context)


@login_required
def main_storage(request):
    """The `main_storage` view function is responsible for handling the display of
    all phones in the main storage.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members
      are allowed to access this view.
    - Renders the main storage page, displaying all phones in the main storage.
    - Implements search and filtering functionality.
    - Implements pagination functionality.

    Note:
    This view assumes user authentication and validation of staff status have been
    handled in the authentication system and UserProfile model.
    """
    content = None
    if request.user.is_staff:
        user = request.user
        queryset = MainStorage.objects.filter(in_stock=True, sold=False,
                                              assigned=False).order_by('id')
        filter = FilterMainStorege(request.GET, queryset=queryset)
        if filter.is_valid():
            queryset = filter.qs
        if request.method == 'POST':
            search_query = request.POST.get('search_query', None)
            if search_query:
                queryset = search(search_query)
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        content = {'data': queryset,
                   'filter': filter,
                   'profile': user.email[0],
                   'avatar': avatar}
    return render(request, 'users/admin_sites/main_stock.html', content)


def agents_and_data(request):
    """The `agents_and_data` view function is responsible for handling the display of
    all agents and their phone data.
    """
    data_by_agent = {}
    content = None

    if request.user.is_staff:
        user = request.user
        queryset = MainStorage.objects.all().order_by('id')
        agents = AgentProfile.objects.all().order_by('id')
        filter = FilterAgentAndData(request.GET, queryset=AgentProfile.objects.all().order_by('id'))
        if filter.is_valid():
            agents = filter.qs
        for agent in agents:
            data_by_agent[agent] = list(queryset.filter(agent=agent.user.id, in_stock=True))
        avatar = UserAvatar.objects.get(user=request.user)
        content = {
                   'data_by_agent': data_by_agent,
                   'filter': filter,
                   'profile': user.email[0],
                    'avatar': avatar}
    return render(request, 'users/admin_sites/admin_agent_view.html', content)