#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the dashboard view function, which is the main entry point
for authenticated users into the application.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.agent_profile import AgentProfile
from ..models.agent_profile import Agent_sign_up_code
from ..models.user_profile import UserAvatar, UserProfile
from uuid import uuid4
from django.shortcuts import redirect
from ..models.main_storage import MainStorage, Airtel_mifi_storage
from ..models.customer_details import CustomerData
from django.utils import timezone



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
        agent_code = Agent_sign_up_code.objects.all()
        try:
            if agent_code[0].used == False:
                agent_code = agent_code[0].code
            else:
                agent_code = "No code available"
        except IndexError:
            agent_code = "No code available"

        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        context = {
            'profile': user.email[0],
            'user': user,
            'agent_code': agent_code,
            'avatar': avatar
        }
        return render(request, 'users/admin_sites/main.html', context)
    elif request.user.groups.filter(name='staff_members').exists():
        user = request.user
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        current_week = timezone.now().date()
        monday = current_week - timezone.timedelta(days=current_week.weekday())
        sunday = monday + timezone.timedelta(days=6)
        customers = CustomerData.objects.filter(created_at__range=[monday, sunday]).order_by('-created_at')
        customers = [(customer, list(customer.phonedata_set.all())) for customer in customers]
        context = {
            'customers': customers,
            'profile': user.email[0],
            'user': user,
            'avatar': avatar
        }
        return render(request, 'users/staff_sites/staff.html', context)
    elif request.user.groups.filter(name='agents').exists():
        user = request.user
        agent_profile = AgentProfile.objects.get(user=user)
        if agent_profile:
            current_month = timezone.now().date().month
            current_year = timezone.now().date().year
            stock_out = MainStorage.objects.filter(agent=user, in_stock=False,
                                                   assigned=True,
                                                   stock_out_date__month=current_month,
                                                   stock_out_date__year=current_year)
            stock_in = MainStorage.objects.filter(agent=user, in_stock=True, assigned=True)
            pending = MainStorage.objects.filter(agent=user, in_stock=False, assigned=False,
                                                sales_type='Loan', contract_no=None)
            avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
            context = {
                'profile': user.email[0],
                'user': user,
                'stock_out': stock_out,
                'stock_in': stock_in,
                'total_stock_in': len(stock_in),
                'total_stock_out': len(stock_out),
                'pending': len(pending),
                'avatar': avatar
            }
        return render(request, 'users/agent_sites/agents.html', context)
    elif request.user.groups.filter(name='airtel_agents').exists():
        stock_in = Airtel_mifi_storage.objects.filter(agent=request.user, in_stock=True)
        stock_out = Airtel_mifi_storage.objects.filter(agent=request.user, in_stock=False)
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        context = {
            'profile': request.user.email[0],
            'user': request.user,
            'stock_in': stock_in,
            'stock_out': stock_out,
            'total_stock_in': len(stock_in),
            'total_stock_out': len(stock_out),
            'avatar': avatar
        }
        return render(request, 'users/airtel_agents/airtel_agents.html', context)
    
    elif request.user.groups.filter(name='Airtel_Supervisor').exists():
        airtel_agents = UserProfile.objects.filter(groups__name='airtel_agents')
        total_sales_by_agents = {}
        for agent in airtel_agents:
            total_sales_by_agents[agent] = len(Airtel_mifi_storage.objects.filter(agent=agent.id,
                                                                                 in_stock=True, pending=True))
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        context = {
            'profile': request.user.email[0],
            'user': request.user,
            'airtel_agents': airtel_agents,
            'total_sales_by_agents': total_sales_by_agents,
            'avatar': avatar
        }
        return render(request, 'users/airtel_supervisor/dashboard.html', context) 
    else:
        return render(request, 'users/regular_user.html', {'user': request.user})
    

@login_required
def generate_agent_code(request):
    """
    The `generate_agent_code` view function is used to generate a new agent sign up code.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Generates a new agent sign up code.
    - Saves the agent sign up code to the database.
    - Renders the dashboard page, providing access to various application features.
    - May include different views, options, and functionalities based on user roles.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the application's dashboard page.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to generate a new agent sign up code.
    - Customizes the dashboard interface based on user roles and permissions.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.user.is_staff:
        code = str(uuid4())[:15]
        exist_code = Agent_sign_up_code.objects.all()
        if exist_code:
            exist_code.update(code=code, used=False)
        else:
            Agent_sign_up_code.objects.create(code=code, used=False)
    return redirect('dashboard')