#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the dashboard view function, which is the main entry point
for authenticated users into the application.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.agent_profile import AgentProfile
from ..models.user_profile import UserAvatar, UserProfile
from ..data_analysis_engine.admin_panel.calc_commitions import CalcCommissions
from ..models.main_storage import MainStorage, Airtel_mifi_storage
from django.utils import timezone
from webpush import send_user_notification
from django.shortcuts import redirect
import os


@login_required
def dashboard(request):
    """
    The `dashboard` view function is the main entry point for authenticated users
    into the application's dashboard.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Renders the dashboard page, providing access to various application features.
    - May include different views, options, and functionalities based on user roles.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the application's dashboard page.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to interact with the application's core
      functionalities.
    - Customizes the dashboard interface based on user roles and permissions.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.user.is_staff:
        user = request.user
        admin_url = '/' + os.environ.get('ADMIN_URL') + '/'
        avatar = UserAvatar.objects.get(
            user=request.user) if UserAvatar.objects.filter(
                user=request.user).exists() else None
        context = {
            'profile': user.email[0],
            'user': user,
            'admin_url': admin_url,
            'avatar': avatar,
        }
        return render(request, 'users/admin_sites/main.html', context)
    elif request.user.groups.filter(name='staff_members').exists():
        user = request.user
        avatar = UserAvatar.objects.get(
            user=request.user) if UserAvatar.objects.filter(
                user=request.user).exists() else None
        mbos = UserProfile.objects.filter(groups__name='MBOs').all()
        context = {
            'profile': user.email[0],
            'user': user,
            'avatar': avatar,
            'mbos': mbos
        }
        return render(request, 'users/staff_sites/staff.html', context)
    elif request.user.groups.filter(name='agents').exists():
        user = request.user
        agent_profile = AgentProfile.objects.get(user=user)
        if agent_profile:
            current_month = timezone.now().date().month
            current_year = timezone.now().date().year
            stock_out = MainStorage.objects.filter(
                agent=user, in_stock=False,
                assigned=True,
                stock_out_date__month=current_month,
                stock_out_date__year=current_year,
                pending=False, sold=True, issue=False,
                faulty=False, recieved=True).count()
            stock_in = MainStorage.objects.filter(
                agent=user, in_stock=True, assigned=True,
                pending=False, issue=False, sold=False,
                recieved=True, faulty=False, paid=False).count()
            CalcCommissions().update_commission(
                user, stock_out
            )
            progress, target = CalcCommissions().target_progress(user)
            avatar = UserAvatar.objects.get(
                user=request.user) if UserAvatar.objects.filter(
                    user=request.user).exists() else None
            context = {
                'profile': user.email[0],
                'user': user,
                'total_stock_in': stock_in,
                'total_stock_out': stock_out,
                'avatar': avatar,
                'progress': progress,
                'target': target,
                'commission': CalcCommissions().calc_commission(user)
            }
        return render(request, 'users/agent_sites/agents.html', context)
    elif request.user.groups.filter(name='MBOs').exists():
        user = request.user
        avatar = UserAvatar.objects.get(
            user=request.user) if UserAvatar.objects.filter(
                user=request.user).exists() else None
        context = {
            'profile': user.email[0],
            'user': user,
            'avatar': avatar
        }
        return render(request, 'users/mbos/mbos.html', context)
    elif request.user.groups.filter(name='airtel').exists():
        user = request.user
        avatar = UserAvatar.objects.get(
            user=request.user) if UserAvatar.objects.filter(
                user=request.user).exists() else None
        context = {
            'profile': user.email[0],
            'user': user,
            'avatar': avatar
        }
        return render(request, 'users/airtel_sites/dashboard.html', context)
    return redirect('sign_in')
