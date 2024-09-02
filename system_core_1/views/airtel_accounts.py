"""This view function is responsible for assigning a promoter to an Airtel device."""
from ..models.user_profile import UserProfile
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from ..models.main_storage import Airtel_mifi_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Case, When, IntegerField
from django.http import JsonResponse


@login_required
def promoters_data(request):
    """This view returns data of promoters as JSON with pagination."""

    # Check if the user is authenticated and belongs to the 'airtel' group
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        
        # Aggregate data using Django's annotate() to minimize database queries
        promoters = UserProfile.objects.filter(groups__name='promoters').annotate(
            within_due_date=Count(
                Case(
                    When(
                        airtel_mifi_storage__in_stock=True, 
                        airtel_mifi_storage__payment_confirmed=False, 
                        airtel_mifi_storage__paid=False,
                        airtel_mifi_storage__activated=False, 
                        airtel_mifi_storage__next_due_date__gt=timezone.now(),
                        then=1
                    ),
                    output_field=IntegerField()
                )
            ),
            missed_due_date=Count(
                Case(
                    When(
                        airtel_mifi_storage__in_stock=True, 
                        airtel_mifi_storage__payment_confirmed=False, 
                        airtel_mifi_storage__paid=False,
                        airtel_mifi_storage__activated=False, 
                        airtel_mifi_storage__next_due_date__lte=timezone.now(),
                        then=1
                    ),
                    output_field=IntegerField()
                )
            ),
            total_devices=Count(
                Case(
                    When(
                        airtel_mifi_storage__in_stock=True,
                        then=1
                    ),
                    output_field=IntegerField()
                )
            )
        ).order_by('first_name')

        # Prepare data for JSON response
        data_by_promoters = []
        for promoter in promoters:
            promoters_data = {
                'promoter': {
                    'id': promoter.id,
                    'first_name': promoter.first_name,
                    'last_name': promoter.last_name,
                },
                'within_due_date': promoter.within_due_date,
                'missed_due_date': promoter.missed_due_date,
                'color_code': 'bg-danger' if promoter.missed_due_date > 0 else 'bg-success',
                'in_danger_zone': promoter.missed_due_date > 0,
                'total_devices': promoter.total_devices,
            }
            data_by_promoters.append(promoters_data)

        # Implement pagination
        data_by_promoters = sorted(data_by_promoters, key=lambda x: x['total_devices'], reverse=True)
        paginator = Paginator(data_by_promoters, 12)  # Show 12 promoters per page
        page = request.GET.get('page', 1)
        
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(1)
        except EmptyPage:
            paginated_data = paginator.page(paginator.num_pages)

        # Prepare pagination information
        pagination_info = {
            'current_page': paginated_data.number,
            'total_pages': paginator.num_pages,
            'has_previous': paginated_data.has_previous(),
            'has_next': paginated_data.has_next(),
            'previous_page_number': paginated_data.previous_page_number() if paginated_data.has_previous() else None,
            'next_page_number': paginated_data.next_page_number() if paginated_data.has_next() else None,
        }

        # Return the JSON response
        return JsonResponse({
            'data_by_promoters': list(paginated_data),  # Convert QuerySet to list for JSON serialization
            'pagination': pagination_info,
        })

    # Return a 403 Forbidden response if the user is not allowed to access this view
    return HttpResponseForbidden()


@login_required
def devices_per_promoter(request, promoter_id):
    """This view function is responsible for displaying the devices per promoter.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Renders the devices per promoter data.

    Parameters:
    - request: The HTTP request object containing user information.
    - fullname: The full name of the promoter.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    - If the staff member is authenticated, it renders the devices per promoter data.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        promoter = UserProfile.objects.get(id=promoter_id)
        total_overdue = 0
        devices = Airtel_mifi_storage.objects.filter(
            promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
            activated=False).all().order_by('next_due_date')
        for device in devices:
            if device.next_due_date.date() > timezone.now().date():
                device.days_left = (device.next_due_date.date() - timezone.now().date()).days + 1
            elif device.next_due_date > timezone.now():
                device.days_after_due = (timezone.now() - device.next_due_date).days
                device.days_left = 0
                total_overdue += 1
            device.save()

        overdue_devices = Airtel_mifi_storage.objects.filter(
            promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
            activated=False, next_due_date__lte=timezone.now()).all().order_by('next_due_date')
        on_time_devices = Airtel_mifi_storage.objects.filter(
            promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
            activated=False, next_due_date__gt=timezone.now()).all().order_by('next_due_date')
        paginator = Paginator(on_time_devices, 9)
        page = request.GET.get('page')
        try:
            on_time_devices = paginator.page(page)
        except PageNotAnInteger:
            on_time_devices = paginator.page(1)
        except EmptyPage:
            on_time_devices = paginator.page(paginator.num_pages)
        return render(request, 'users/airtel_sites/devices_per_promoter.html',
                      {'on_time_devices': on_time_devices, 'total_overdue': total_overdue, 'promoter': promoter,
                       'overdue_devices': overdue_devices})
    return HttpResponseForbidden()


@login_required
def airtel_promoter_accounts(request):
    """This view function is responsible for displaying the Airtel promoter accounts.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Renders the Airtel promoter accounts data.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    - If the staff member is authenticated, it renders the Airtel promoter accounts data.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        return render(request, 'users/airtel_sites/promoters_data.html')
    return HttpResponseForbidden()