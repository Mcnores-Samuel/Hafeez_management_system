#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module contains the views for the application."""
from django.shortcuts import render
from ..forms import *
from ..models import AgentProfile
from django.contrib.auth.decorators import login_required
from ..models.agent_profile import AgentProfile
from ..models.user_profile import UserProfile
from ..models.main_storage import MainStorage
from ..forms.filters import FilterMainStorege
from ..forms.filters import FilterAgentAndData
from ..models.user_profile import UserAvatar
from .search_and_filters import search


@login_required
def users(request):
    """The `users` view function is responsible for handling the display of all users
    in the application.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members
      are allowed to access this view.
    - Renders the users page, displaying all users in the application.
    """
    content = None
    if request.user.is_staff:
        user = request.user
        all_users = UserProfile.objects.all().order_by('id')
        agents = AgentProfile.objects.all().order_by('id')
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        content = {'users': all_users,
                   'agents': agents,
                   'profile': user.email[0],
                   'avatar': avatar}
    return render(request, 'users/admin_sites/users.html', content)


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