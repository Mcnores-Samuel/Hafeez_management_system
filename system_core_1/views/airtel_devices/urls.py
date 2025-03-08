from django.urls import path
from system_core_1.views.airtel_devices.create_new_promoter import create_new_promoter
from system_core_1.views.airtel_devices.airtel_device_destributer import search_airtel_devices, assignPromoter
from system_core_1.views.airtel_devices.airtel_accounts import promoters_data, devices_per_promoter, airtel_promoter_accounts, paymentsNotification
from system_core_1.views.airtel_devices.airtel_dev_ops import return_device, edit_device, sale_device, reset_device
from system_core_1.views.airtel_devices.airtel_admin_ops import airtel_devices_data, airtel_device_data_entry, metrics
from system_core_1.views.data_input.recordairteldevices_payment import record_airtel_devices_payment
from system_core_1.views.airtel_devices.add_airtel_devices_stock import add_airtel_devices_stock
from system_core_1.views.airtel_devices.admin_airtel_payments import currentPayments, renewPayment, concludedPayments, deletePayment

urlpatterns = [
    path('add_airtel_devices_stock/', add_airtel_devices_stock, name='add_airtel_devices_stock'),
    path('create_new_promoter/', create_new_promoter, name='create_new_promoter'),
    path('search_airtel_devices/', search_airtel_devices, name='search_airtel_devices'),
    path('promoters_data/', promoters_data, name='promoters_data'),
    path('paymentsNotification/<int:note_id>', paymentsNotification, name='paymentsNotification'),
    path('paymentsNotification/', paymentsNotification, name='paymentsNotification'),
    path('airtel_promoter_accounts/', airtel_promoter_accounts, name='airtel_promoter_accounts'),
    path('devices_per_promoter/<int:promoter_id>/', devices_per_promoter, name='devices_per_promoter'),
    path('assignPromoter/', assignPromoter, name='assignPromoter'),
    path('return_device/', return_device, name='return_device'),
    path('edit_device/', edit_device, name='edit_device'),
    path('sale_device/', sale_device, name='sale_device'),
    path('reset_device/', reset_device, name='reset_device'),
    path('airtel_devices_data/', airtel_devices_data, name='airtel_devices_data'),
    path('airtel_device_data_entry/', airtel_device_data_entry, name='airtel_device_data_entry'),
    path('record_airtel_devices_payment/', record_airtel_devices_payment, name='record_airtel_devices_payment'),
    path('currentPayments/', currentPayments, name='currentPayments'),
    path('renewPayment/', renewPayment, name='renewPayment'),
    path('concludedPayments/', concludedPayments, name='concludedPayments'),
    path('deletePayment/', deletePayment, name='deletePayment'),
    path('metrics/', metrics, name='metrics'),
]
