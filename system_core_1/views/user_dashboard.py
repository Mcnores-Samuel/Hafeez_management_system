#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the dashboard view function, which is the main entry point
for authenticated users into the application.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.agent_profile import AgentProfile
from ..models.agent_stock import AgentStock
from ..models.agent_profile import Agent_sign_up_code
from uuid import uuid4
from django.shortcuts import redirect


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

        context = {
            'profile': user.email[0],
            'user': user,
            'agent_code': agent_code
        }
        return render(request, 'users/main.html', context)
    elif request.user.groups.filter(name='agents').exists() or request.user.is_superuser:
        user = request.user
        agent_profile = AgentProfile.objects.get(user=user)
        stock_out = AgentStock.objects.filter(agent=agent_profile, in_stock=False)
        stock_in = AgentStock.objects.filter(agent=agent_profile, in_stock=True)
        pending = AgentStock.objects.filter(agent=agent_profile, in_stock=False,
                                             sales_type='Loan', contract_number=None)
        context = {
            'profile': user.email[0],
            'user': user,
            'stock_out': stock_out,
            'stock_in': stock_in,
            'total_stock_in': len(stock_in),
            'total_stock_out': len(stock_out),
            'pending': len(pending)
        }
        return render(request, 'users/agents.html', context)
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