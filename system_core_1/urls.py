from django.urls import path
from django.contrib.auth import views as auth_views
from .views.data_input import sales_register
from .views import (registration_view, data_updates, central_display, home_page, user_dashboard, action_on_data_select, search_and_filters)

from .views.data_input.feedback import feedback
from .views.data_input.add_to_stock import (add_to_stock, add_accessaries, add_appliances, add_refarbished)
from .views.pending_sales import total_pending_sales, revert_to_stock, pending_sales, pending_sales_details
from .views.defects import defects
from .views.agents import agents_data_access
from .views.system_routine_updates import (morning_update, afternoon_update, evening_update)
from .views.accounts_and_data import dataAccess, sales_stock_summry, dailySalesByShop
from .views.data_input.stock_taking import stock_taking
from system_core_1.views.data_input.dispatch import dispatch_stock
from system_core_1.views.airtel_devices.urls import urlpatterns as airtel_devices_urls
from system_core_1.views.accounting.urls import urlpatterns as accounting_urls
from system_core_1.views.ex_rate_pricing.admin_views.urls import urlpatterns as ex_rate_pricing_urls
from system_core_1.views.api.v1.urls import urlpatterns as api_v1_urls
from system_core_1.views.analytics.urls import urlpatterns as analytics_urls
import itertools

urlpatterns = list(itertools.chain(
    airtel_devices_urls, accounting_urls,
    ex_rate_pricing_urls, api_v1_urls,
    analytics_urls
    ))

urlpatterns += [
    # home page
    path('', home_page.home_page, name='home_page'),

    # registration
    path('sign_in/', registration_view.sign_in, name='sign_in'),
    path('sign_out/', registration_view.sign_out, name='sign_out'),
    # Data on actions on data and admin panel
    path('dashboard/', user_dashboard.dashboard, name='dashboard'),
    path('main_stock_details/', central_display.main_stock_details, name='main_stock_details'),
    path('main_sales_details/', central_display.main_sales_details, name='main_sales_details'),
    path('dispatch_stock/', dispatch_stock, name='dispatch_stock'),
    path('uploadBulkSales/', sales_register.uploadBulkSales, name='uploadBulkSales'),
    path('accessary_sales', sales_register.accessary_sales, name='accessary_sales'),
    path('appliance_sales', sales_register.appliance_sales, name='appliance_sales'),
    path('refarbished_sales', sales_register.refarbished_sales, name='refarbished_sales'),
    path('stock_taking/', stock_taking, name='stock_taking'),
    path('revert_to_stock/', revert_to_stock, name='revert_to_stock'),
    path('pending_sales/', pending_sales, name='pending_sales'),
    path('pending_sales_details/<str:username>/', pending_sales_details, name='pending_sales_details'),
    path('defects/', defects, name='defects'),
    # General access points
    path('profile/', data_updates.profile, name='profile'),
    path('feedback/', feedback, name='feedback'),
    path('add_to_stock/', add_to_stock, name='add_to_stock'),
    path('add_accessaries/', add_accessaries, name='add_accessaries'),
    path('add_appliances/', add_appliances, name='add_appliances'),
    path('add_refarbished/', add_refarbished, name='add_refarbished'),
    path('data_search/', search_and_filters.data_search, name='data_search'),
    path('verify_stock_recieved/', data_updates.verify_stock_recieved, name='verify_stock_recieved'),
    path('upload_image/', data_updates.upload_image, name='upload_image'),
    path('change_password/', data_updates.change_password, name='change_password'),
    path('combinedData_collection/<int:data_id>/', sales_register.combinedData_collection, name='combinedData_collection'),
    path('add_contract_number/', data_updates.add_contract_number, name='add_contract_number'),
    # Agents and staff access points
    path('dataAccess/', dataAccess, name='dataAccess'),
    path('dailySalesByShop/', dailySalesByShop, name='dailySalesByShop'),
    path('sales_stock_summry/', sales_stock_summry, name='sales_stock_summry'),
    path('verify_stock_recieved/', data_updates.verify_stock_recieved, name='verify_stock_recieved'),
    path('in_stock/', data_updates.in_stock, name='in_stock'),
    path('stock_out/', data_updates.stock_out, name='stock_out'),
    path('my_pending_sales/', agents_data_access.my_pending_sales, name='my_pending_sales'),
    path('new_stock/', agents_data_access.new_stock, name='new_stock'),
    path('sale_on_cash', action_on_data_select.sale_on_cash, name='sale_on_cash'),
    path('sale_on_loan/<int:data_id>/', action_on_data_select.sale_on_loan, name='sale_on_loan'),
    # Concurent system operations with data analysis
    path('total_pending_sales/', total_pending_sales, name='total_pending_sales'),
    #system email and notifications auto updates
    path('morning_update/', morning_update, name='morning_update'),
    path('afternoon_update/', afternoon_update, name='afternoon_update'),
    path('evening_update/', evening_update, name='evening_update'),
    # reseting user password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
]