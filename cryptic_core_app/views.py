from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import *
from django.urls import reverse
from .models import AgentProfile
from django_email_verification import send_email
from django_email_verification import verify_view, verify_token
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import *
from .helper_modules.load_json_file import load_from_json_file
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password


def home_page(request):
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
    success, user = verify_token(token)
    return HttpResponse(f'Account verified, {user.username}' if success else 'Invalid token')


def sign_up(request):
    """
    The `sign_up` view function handles user registration and sign-up processes.

    Functionality:
    - Allows users to create new accounts by providing necessary registration details.
    - Validates user input, ensuring it meets specified criteria.
    - Upon successful registration, creates a new user account and redirects to the
      sign-in page.

    Parameters:
    - request: The HTTP request object containing user registration data.

    Returns:
    - Renders the registration form for users to input their registration details.
    - Redirects to the sign-in page after successful registration.

    Usage:
    - Users access this view to create new accounts within the application.
    - Ensures a seamless registration process while maintaining data integrity.

    Note:
    - User authentication and validation logic should be implemented in the associated
      authentication system.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data["role"]
            if role == 'regular':
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                send_email(user)
                return redirect(reverse('sign_in'))
            elif role == 'agent':
                agent_code = form.cleaned_data['agent_code']
                filename = "cryptic_core_app/protected_codes/agent_code.json"
                if agent_code == load_from_json_file(filename):
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    agen_group = Group.objects.get(name="agents")
                    user.groups.add(agen_group)
                    agent_profile = AgentProfile.objects.create(user=user)
                    agent_profile.is_agent = True
                    send_email(user)
                    return redirect(reverse('sign_in'))
                else:
                    form.add_error('agent_code', "Invalid code!!, please Enter a valid code")
    else:
        form = SignUpForm()
    return render(request, 'authentication/sign_up.html', {'form': form})


def sign_in(request):
    """
    The `sign_in` view function handles user authentication and sign-in processes.

    Functionality:
    - Allows registered users to sign in by providing their credentials (e.g., email
      and password).
    - Validates user credentials and, upon success, grants access to the application.
    - Displays appropriate error messages in case of unsuccessful sign-in attempts.

    Parameters:
    - request: The HTTP request object containing user authentication data.

    Returns:
    - Renders the sign-in form for users to input their credentials.
    - Grants access to the application dashboard upon successful sign-in.
    - Displays error messages for invalid sign-in attempts.

    Usage:
    - Registered users access this view to log in and access the application's features.
    - Includes user authentication and session management logic.

    Note:
    - User authentication and validation should be handled by the authentication system.
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
    return render(request, 'authentication/sign_in.html', {'form': form})


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
        context = {
            'profile': user.email[0],
            'user': user
        }
        return render(request, 'users/main.html', context)
    elif request.user.groups.filter(name='agents').exists():
        user = request.user
        agent_profile = AgentProfile.objects.get(user=user)
        stock_out = AgentStock.objects.filter(agent=agent_profile, in_stock=False)
        stock_in = AgentStock.objects.filter(agent=agent_profile, in_stock=True)
        context = {
            'profile': user.email[0],
            'user': user,
            'stock_out': stock_out,
            'stock_in': stock_in
        }
        return render(request, 'users/agents.html', context)
    else:
        return render(request, 'users/regular_user.html', {'user': request.user})

@login_required
def sign_out(request):
    logout(request)
    return redirect('/')


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(user)
    
    context = {
        'password_form': password_form,
    }
    
    return render(request, 'users/change_password.html', context)


@login_required
def profile(request):
    user = request.user
    profile_form = None
    if request.method == 'POST':
        if 'first_name' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile information was successfully updated.')
                return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user)
    context = {
            'profile': user.email[0],
            'user': user,
            'profile_form': profile_form,
        }
    return render(request, 'users/profile.html', context)


def combinedData_collection(request, data_id):
    """
    The `combinedData_collection` view function is a Django view responsible for
    handling the collection of customer and phone data during the phone purchasing
    process by agents.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Verifies if the agent has available stock of phones.
    - Renders either the combined data form or an "out of stock" message based on
      the agent's stock availability.
    - If the agent has stock and submits the form, customer and phone records are
      created in the database.
    - If the agent is out of stock, a message is displayed, instructing them to
      contact the office for stock replenishment.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it renders the combined data form.
    - If the agent is out of stock, it renders an "out of stock" message.

    Usage:
    Agents access this view to collect customer data and select phones for sale.
    It ensures that agents with available stock can proceed with data collection,
    while agents without stock are notified to contact the office for replenishment.

    Note:
    This view assumes user authentication and validation of agent status have been
    handled in the authentication system and AgentProfile model.
    """
    if request.user.is_authenticated and request.user.agentprofile.is_agent:
        agent_profile = request.user.agentprofile
        has_stock = AgentStock.objects.filter(agent=agent_profile, in_stock=True)
        if has_stock:
            if request.method == 'POST':
                form = CombinedDataForm(request.POST, user=request.user)
                if form.is_valid():
                    payment_method = form.cleaned_data['payment_method']
                    if payment_method == 'Cash':
                        phone_data = form.process_cash_payment(data_id)
                        return redirect('dashboard')
                    elif payment_method == 'Loan':
                        customer_data, phone_data = form.process_loan_payment(data_id)
                        return redirect('dashboard')
            else:
                form = CombinedDataForm(user=request.user)
            return render(request, 'registration/collect_customer_data.html', {'form': form})
        else:
            return render(request, 'authentication/out_of_stock.html')
    else:
        return HttpResponseForbidden("Access Denied")