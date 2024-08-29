from ..models.main_storage import Airtel_mifi_storage
from django.contrib.auth.decorators import login_required
from ..models.user_profile import UserProfile
from django.utils import timezone
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def airtel_devices_data(request):
    if request.user.is_superuser:
        promoters = UserProfile.objects.filter(groups__name='promoters').all().order_by('first_name')
        data_by_promoters = []
        promoters_data = {}
        for promoter in promoters:
            promoters_data['promoter'] = promoter
            promoters_data['total_devices'] = Airtel_mifi_storage.objects.filter(
                promoter=promoter, in_stock=True).count()
            promoters_data['todays_collection'] = Airtel_mifi_storage.objects.filter(
                promoter=promoter, in_stock=True, payment_confirmed=True, paid=True, activated=True,
                collected_on__date=timezone.now().date()).count()
            promoters_data['within_due_date'] = Airtel_mifi_storage.objects.filter(
                promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
                activated=False, next_due_date__gt=timezone.now()).count()
            promoters_data['missed_due_date'] = Airtel_mifi_storage.objects.filter(
                promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
                activated=False, next_due_date__lte=timezone.now()).count()
            data_by_promoters.append(promoters_data)
            promoters_data = {}

        paginator = Paginator(data_by_promoters, 15)
        page = request.GET.get('page')
        try:
            data_by_promoters = paginator.page(page)
        except PageNotAnInteger:
            data_by_promoters = paginator.page(1)
        except EmptyPage:
            data_by_promoters = paginator.page(paginator.num_pages)
        return render(request, 'users/admin_sites/airtel_devices_data.html', {'data_by_promoters': data_by_promoters})
    


@login_required
def payment_confirmation(request, promoter_id):
    if request.user.is_superuser:
        promoter = UserProfile.objects.get(id=promoter_id)
        return render(request, 'users/admin_sites/payment_confirmation.html')