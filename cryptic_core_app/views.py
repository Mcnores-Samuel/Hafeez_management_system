from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import *
from django.urls import reverse
from .models import AgentProfile
from django_email_verification import verify_view, verify_token
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .helper_modules.load_json_file import load_from_json_file


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
        filename = "cryptic_core_app/protected_codes/agent_code.json"
        agent_code = load_from_json_file(filename=filename)
        context = {
            'profile': user.email[0],
            'user': user,
            'agent_code': agent_code
        }
        return render(request, 'users/main.html', context)
    elif request.user.groups.filter(name='agents').exists():
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
def sign_out(request):
    logout(request)
    return redirect(reverse('home_page'))


@login_required
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
    

@login_required
def users(request):
    content = None
    if request.user.is_staff:
        all_users = UserProfile.objects.all().order_by('id')
        agents = AgentProfile.objects.all().order_by('id')
        content = {'users': all_users, 'agents': agents}
    return render(request, 'users/users.html', content)


@login_required
def main_storage(request):
    content = None
    if request.user.is_staff:
        data = MainStorage.objects.all().order_by('id')
        content = {'data': data}
    return render(request, 'users/main_stock.html', content)


from django.db.models import Sum

def agents_and_data(request):
    content = None
    data_by_agent = {}
    
    if request.user.is_staff:
        # Group by 'agent' and calculate the sum of 'stock_quantity' for each group
        data = AgentStock.objects.values('agent').annotate(total_stock_quantity=Sum('agent'))

        # Convert the queryset into a dictionary for easier access in the template
        for entry in data:
            agent_name = entry['agent']
            total_stock = entry['total_stock_quantity']
            data_by_agent[agent_name] = total_stock

        content = {'data_by_agent': data_by_agent}
        print(data_by_agent)

    return render(request, 'users/admin_agent_view.html', content)

    