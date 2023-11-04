from ..forms.sign_up_form import SignUpForm
from ..forms.sign_in_form import SignInForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django_email_verification import send_email
from django.contrib.auth.models import Group
from ..models.agent_profile import AgentProfile
from ..models.agent_profile import Agent_sign_up_code
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



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
                return render(request, 'authentication/confirm_email.html', {'user': user})
            elif role == 'agent':
                agent_code = form.cleaned_data['agent_code']
                sign_up_code = Agent_sign_up_code.objects.filter(code=agent_code, used=False)
                if sign_up_code:
                    sign_up_code.update(used=True)
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    send_email(user)
                    agen_group = Group.objects.get(name="agents")
                    user.groups.add(agen_group)
                    agent_profile = AgentProfile.objects.create(user=user)
                    agent_profile.is_agent = True
                    return render(request, 'authentication/confirm_email.html', {'user': user})
                else:
                    form.add_error(None, "Invalid Agent code!!, please Enter a valid code")
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
    user = None
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if remember_me:
                        request.session.set_expiry(604800)
                    else:
                        request.session.set_expiry(0)
                    if user.is_staff:
                        return redirect(reverse('dashboard'))
                    elif user.groups.filter(name='staff_members').exists():
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
    return render(request, 'authentication/sign_in.html', {'form': form, 'user': user})

@login_required
def resend_confirmation_email(request):
    user = request.user
    if not user.is_active:
        send_email(user)
    return render(request, 'authentication/confirm_email.html')


@login_required
def sign_out(request):
    """The `sign_out` view function is responsible for handling user sign-out.
    """
    logout(request)
    return redirect(reverse('home_page'))