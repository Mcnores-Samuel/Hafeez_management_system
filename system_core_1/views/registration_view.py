# The `registration_view` module contains view functions for user registration and authentication.
from ..forms.sign_in_form import SignInForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages


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
        try:
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
                            if user.last_login:
                                messages.success(request, 'Welcome back, {}'.format(user.username))
                            else:
                                messages.success(request, 'Welcome, {}'.format(user.username))
                            return redirect(reverse('dashboard'))
                        elif user.groups.filter(name='staff_members').exists():
                            if user.last_login:
                                messages.success(request, 'Welcome back, {}'.format(user.username))
                            else:
                                messages.success(request, 'Welcome, {}'.format(user.username))
                            return redirect(reverse('dashboard'))
                        elif user.groups.filter(name='agents').exists():
                            if user.last_login:
                                messages.success(request, 'Welcome back, {}'.format(user.username))
                            else:
                                messages.success(request, 'Welcome, {}'.format(user.username))
                            return redirect(reverse('dashboard'))
                        else:
                            if user.last_login:
                                messages.success(request, 'Welcome back, {}'.format(user.username))
                            else:
                                messages.success(request, 'Welcome, {}'.format(user.username))
                            return redirect(reverse('dashboard'))
                    else:
                        form.add_error(None, "Please!! activate your account")
                else:
                    form.add_error(None, "Invalid username or password")
        except Exception:
            form = SignInForm()
            messages.error(request, 'Something went wrong, please try again')
            return render(request, 'authentication/sign_in.html', {'form': form, 'user': user})
    else:
        form = SignInForm()
    return render(request, 'authentication/sign_in.html', {'form': form, 'user': user})



@login_required
def sign_out(request):
    """The `sign_out` view function is responsible for handling user sign-out.
    """
    logout(request)
    return redirect(reverse('home_page'))
