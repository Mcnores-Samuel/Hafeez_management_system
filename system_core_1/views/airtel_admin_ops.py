from django.http import JsonResponse
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.main_storage import Airtel_mifi_storage
from ..models.user_profile import UserProfile
from django.shortcuts import render
from django.http import HttpResponseForbidden


@login_required
def airtel_devices_data(request):
    if request.user.is_superuser:
        promoters = None
        searchQuery = request.GET.get('search_query')
        if searchQuery:
            searchQuery = ' '.join(searchQuery.split()).strip()
            first_name, last_name = tuple(searchQuery.split(' ', maxsplit=1)) if ' ' in searchQuery else (searchQuery, '')
            promoters = UserProfile.objects.filter(
                groups__name='promoters', first_name__icontains=first_name,
                last_name__icontains=last_name).all().order_by('first_name').select_related()
        else:
            promoters = UserProfile.objects.filter(groups__name='promoters').all().order_by('first_name').select_related()

        # Use aggregation to count related Airtel_mifi_storage objects
        today = timezone.now().date()

        data_by_promoters = promoters.annotate(
            total_devices=Count('airtel_mifi_storage', filter=Q(airtel_mifi_storage__in_stock=True)),
            todays_collection=Count('airtel_mifi_storage', filter=Q(
                airtel_mifi_storage__in_stock=True,
                airtel_mifi_storage__payment_confirmed=True,
                airtel_mifi_storage__paid=True,
                airtel_mifi_storage__activated=True,
                airtel_mifi_storage__collected_on__date=today
            )),
            within_due_date=Count('airtel_mifi_storage', filter=Q(
                airtel_mifi_storage__in_stock=True,
                airtel_mifi_storage__payment_confirmed=False,
                airtel_mifi_storage__paid=False,
                airtel_mifi_storage__activated=False,
                airtel_mifi_storage__next_due_date__gt=timezone.now()
            )),
            missed_due_date=Count('airtel_mifi_storage', filter=Q(
                airtel_mifi_storage__in_stock=True,
                airtel_mifi_storage__payment_confirmed=False,
                airtel_mifi_storage__paid=False,
                airtel_mifi_storage__activated=False,
                airtel_mifi_storage__next_due_date__lte=timezone.now()
            )),
            mifi=Count('airtel_mifi_storage', filter=Q(airtel_mifi_storage__in_stock=True, airtel_mifi_storage__device_type='MIFI')),
            idu=Count('airtel_mifi_storage', filter=Q(airtel_mifi_storage__in_stock=True, airtel_mifi_storage__device_type='IDU'))
        )

        data_by_promoters = sorted(data_by_promoters, key=lambda x: x.total_devices, reverse=True)

        # Pagination
        paginator = Paginator(data_by_promoters, 15)
        page = request.GET.get('page')
        
        try:
            data_by_promoters = paginator.page(page)
        except PageNotAnInteger:
            data_by_promoters = paginator.page(1)
        except EmptyPage:
            data_by_promoters = paginator.page(paginator.num_pages)

        # Prepare JSON data
        data = []
        for promoter_data in data_by_promoters:
            data.append({
                'promoter': {
                    'id': promoter_data.id,
                    'first_name': promoter_data.first_name,
                    'last_name': promoter_data.last_name
                },
                'total_devices': promoter_data.total_devices,
                'todays_collection': promoter_data.todays_collection,
                'within_due_date': promoter_data.within_due_date,
                'missed_due_date': promoter_data.missed_due_date,
                'mifi': promoter_data.mifi,
                'idu': promoter_data.idu,
                'bg': 'red' if promoter_data.missed_due_date > 0 else 'default',
            })

        # Add pagination info
        response_data = {
            'data_by_promoters': data,
            'pagination': {
                'has_previous': data_by_promoters.has_previous(),
                'has_next': data_by_promoters.has_next(),
                'previous_page_number': data_by_promoters.previous_page_number() if data_by_promoters.has_previous() else None,
                'next_page_number': data_by_promoters.next_page_number() if data_by_promoters.has_next() else None,
                'current_page': data_by_promoters.number,
                'total_pages': paginator.num_pages
            }
        }

        # Return JSON response
        return JsonResponse(response_data)
    return HttpResponseForbidden()


@login_required
def airtel_device_data_entry(request):
    if request.user.is_superuser:
        promoters = UserProfile.objects.filter(groups__name='promoters').all().order_by('first_name')
        total_promoters = promoters.count()
        return render(request, 'users/admin_sites/airtel_devices_data.html',
                      {'promoters': promoters, 'total_promoters': total_promoters})