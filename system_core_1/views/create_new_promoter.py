from ..models.user_profile import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib import messages


@login_required
def create_new_promoter(request):
    """This view function is responsible for creating a new promoter.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Renders the create new promoter form.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    - If the staff member is authenticated, it renders the create new promoter form.

    Usage:
    Staff members access this view to create a new promoter.
    It ensures that only staff members are able to access this view.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        team_leaders = UserProfile.objects.filter(groups__name='team_leaders')
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = 'promoter_' + first_name + '.' + last_name + '@system.net'
            phone_number = request.POST.get('phone_number')
            promoter_group = Group.objects.get(name='promoters')
            team_leader = request.POST.get('team_leader')
            location = request.POST.get('residetial_area')
            promoter = UserProfile.objects.create_user(
                email=email, first_name=first_name, last_name=last_name,
                phone_number=phone_number, location=location, team_leader=team_leader,
                is_staff=False, is_active=True, username=first_name)
            promoter.groups.add(promoter_group)
            promoter.save()
            messages.success(request, 'Promoter created successfully')
            return redirect('create_new_promoter')
    return render(request, 'users/airtel_sites/create_new_promoter.html', 
                  {'team_leaders': team_leaders})