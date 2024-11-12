from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (registration_view, data_updates, central_display, home_page, sales_register,
                    user_dashboard, action_on_data_select, search_and_filters, data_for_charts)
from .views.stock_analysis import (get_source_stock, get_yearly_product_sales, admin_stock_analysis)
from .views.feedback import feedback
from .views.add_to_stock import (add_to_stock, add_airtel_devices_stock, add_accessaries,
                                 add_appliances, add_refarbished)
from .views.pending_sales import total_pending_sales, revert_to_stock, pending_sales, pending_sales_details
from .views.defects import defects
from .views import revenues
from .views import agents_data_access
from .views.system_routine_updates import (morning_update, afternoon_update, evening_update)
from .views.create_new_promoter import create_new_promoter
from .views.airtel_device_destributer import search_airtel_devices, assignPromoter
from .views.airtel_accounts import promoters_data, devices_per_promoter, airtel_promoter_accounts, paymentsNotification
from .views.airtel_dev_ops import return_device, edit_device, sale_device, reset_device
from .views.airtel_admin_ops import airtel_devices_data, airtel_device_data_entry, metrics
from .views.recordairteldevices_payment import record_airtel_devices_payment
from .views.sales_update_api import stockQuery, salesUpdates, airtel_sales_data, updateTimeStamp, pendingSales
from .views.accounts_and_data import dataAccess, sales_stock_summry, dailySalesByShop


urlpatterns = [
    # home page
    path('', home_page.home_page, name='home_page'),

    # registration
    path('sign_in/', registration_view.sign_in, name='sign_in'),
    path('sign_out/', registration_view.sign_out, name='sign_out'),
    # data query and update api
    path('stockQuery/', stockQuery, name='stockQuery'),
    path('salesUpdates/', salesUpdates, name='salesUpdates'),
    path('updateTimeStamp/', updateTimeStamp, name='updateTimeStamp'),
    path('pendingSales/', pendingSales, name='pendingSales'),
    path('airtel_sales_data/', airtel_sales_data, name='airtel_sales_data'),
    # Data on actions on data and admin panel
    path('dashboard/', user_dashboard.dashboard, name='dashboard'),
    path('main_stock_details/', central_display.main_stock_details, name='main_stock_details'),
    path('main_sales_details/', central_display.main_sales_details, name='main_sales_details'),
    path('dispatch_stock/', home_page.dispatch_stock, name='dispatch_stock'),
    path('uploadBulkSales/', sales_register.uploadBulkSales, name='uploadBulkSales'),
    path('revenues/', revenues.revenues, name='revenues'),
    path('revert_to_stock/', revert_to_stock, name='revert_to_stock'),
    path('pending_sales/', pending_sales, name='pending_sales'),
    path('pending_sales_details/<str:username>/', pending_sales_details, name='pending_sales_details'),
    path('defects/', defects, name='defects'),
    path('airtel_devices_data/', airtel_devices_data, name='airtel_devices_data'),
    path('airtel_device_data_entry/', airtel_device_data_entry, name='airtel_device_data_entry'),
    path('record_airtel_devices_payment/', record_airtel_devices_payment, name='record_airtel_devices_payment'),
    path('metrics/', metrics, name='metrics'),
    # General access points
    path('profile/', data_updates.profile, name='profile'),
    path('feedback/', feedback, name='feedback'),
    path('add_to_stock/', add_to_stock, name='add_to_stock'),
    path('add_accessaries/', add_accessaries, name='add_accessaries'),
    path('add_appliances/', add_appliances, name='add_appliances'),
    path('add_refarbished/', add_refarbished, name='add_refarbished'),
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
    path('get_daily_sales_json_loan/', data_for_charts.get_daily_sales_json_loan, name='get_daily_sales_json_loan'),
    path('get_daily_sales_json_cash/', data_for_charts.get_daily_sales_json_cash, name='get_daily_sales_json_cash'),
    path('get_weekly_sales_json_loan/', data_for_charts.get_weekly_sales_json_loan, name='get_weekly_sales_json_loan'),
    path('get_weekly_sales_json_cash/', data_for_charts.get_weekly_sales_json_cash, name='get_weekly_sales_json_cash'),
    path('get_sale_by_agent_monthy_loan/', data_for_charts.get_sale_by_agent_monthy_loan, name='get_sale_by_agent_monthy_loan'),
    path('get_sale_by_agent_monthy_cash/', data_for_charts.get_sale_by_agent_monthy_cash, name='get_sale_by_agent_monthy_cash'),
    path('get_individual_agent_stock/', data_for_charts.get_individual_agent_stock, name='get_individual_agent_stock'),
    path('get_individual_agent_stock_out/', data_for_charts.get_individual_agent_stock_out, name='get_individual_agent_stock_out'),
    path('get_agents_stock_json/', data_for_charts.get_agents_stock_json, name='get_agents_stock_json'),
    path('get_source_stock/', get_source_stock, name='get_source_stock'),
    path('get_yearly_product_sales/', get_yearly_product_sales, name='get_yearly_product_sales'),
    path('get_main_stock_analysis/', data_for_charts.get_main_stock_analysis, name='get_main_stock_analysis'),
    path('admin_stock_analysis/', admin_stock_analysis, name='admin_stock_analysis'),
    path('total_pending_sales/', total_pending_sales, name='total_pending_sales'),
    path('get_yearly_sales/', data_for_charts.get_yearly_sales, name='get_yearly_sales'),
    path('get_yearly_sales_total/', data_for_charts.get_yearly_sales_total, name='get_yearly_sales_total'),
    path('agent_daily_sales/', data_for_charts.agent_daily_sales, name='agent_daily_sales'),
    #system email and notifications auto updates
    path('morning_update/', morning_update, name='morning_update'),
    path('afternoon_update/', afternoon_update, name='afternoon_update'),
    path('evening_update/', evening_update, name='evening_update'),
    # Revenue analysis and concurent operations
    path('calculateCreditRevenue/', revenues.calculateCreditRevenue, name='calculateCreditRevenue'),
    path('getCostAndRevenue/', revenues.getCostAndRevenue, name='getCostAndRevenue'),
    # reseting user password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
]