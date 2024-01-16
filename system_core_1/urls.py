from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (registration_view, data_updates, customer_registrar,
                    central_display, home_page, user_dashboard, action_on_data_select,
                    search_and_filters, approve_contracts,
                    data_for_charts)
from .views.staff_sites.approve import (
    approved, get_approved_data, approve, get_total_to_approve)
from .views.staff_sites.new_entries import (get_new_entries, get_new_entries_total, mark_as_read)
from .views.staff_sites.edit_customer_data import edit_customer_data
from .views.staff_sites.delete_data import delete_customer_data
from .views.staff_sites.rejected import total_rejected, get_rejected
from .views.stock_analysis import get_source_stock



urlpatterns = [
    path('', home_page.home_page, name='home_page'),
    path('products/', home_page.products, name='products'),
    path('about/', home_page.about, name='about'),
    path('faq/', home_page.faq, name='faq'),
    path('terms/', home_page.terms, name='terms'),
    path('contact/', home_page.contact, name='contact'),
    path('services/', home_page.services, name='services'),
    path('privacy/', home_page.privacy, name='privacy'),
    path('sign_up/', registration_view.sign_up, name='sign_up'),
    path('main_shop_details/', home_page.main_shop_details, name='main_shop_details'),
    path('resend_confirmation_email', registration_view.resend_confirmation_email, name='resend_confirmation_email'),
    path('generate_agent_code/', user_dashboard.generate_agent_code, name='generate_agent_code'),
    path('sign_in/', registration_view.sign_in, name='sign_in'),
    path('sign_out/', registration_view.sign_out, name='sign_out'),
    path('dashboard/', user_dashboard.dashboard, name='dashboard'),
    path('profile/', data_updates.profile, name='profile'),
    path('change_password/', data_updates.change_password, name='change_password'),
    path('combinedData_collection/<int:data_id>/', customer_registrar.combinedData_collection, name='combinedData_collection'),
    path('add_contract_number/', data_updates.add_contract_number, name='add_contract_number'),
    path('verify_stock_recieved/', data_updates.verify_stock_recieved, name='verify_stock_recieved'),
    path('in_stock/', data_updates.in_stock, name='in_stock'),
    path('stock_out/', data_updates.stock_out, name='stock_out'),
    path('users/', central_display.users, name='users'),
    path('main_storage/', central_display.main_storage, name='main_storage'),
    path('agents_and_data/', central_display.agents_and_data, name='agents_and_data'),
    path('deploy_device/<int:data_id>/', action_on_data_select.deploy_device, name='deploy_device'),
    path('sale_on_cash/<int:data_id>/', action_on_data_select.sale_on_cash, name='sale_on_cash'),
    path('data_search/', search_and_filters.data_search, name='data_search'),
    path('search_customers/', search_and_filters.search_customers, name='search_customers'),
    path('update_customer_data/', data_updates.update_customer_data, name='update_customer_data'),
    path('approve_contracts/', approve_contracts.approve_contracts, name='approve_contracts'),
    path('decline_contracts/', approve_contracts.decline_contracts, name='decline_contracts'),
    path('sale_aitel_device/', approve_contracts.sale_aitel_device, name='sale_aitel_device'),
    # produces data for charts in dashboard
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
    path('get_main_stock_analysis/', data_for_charts.get_main_stock_analysis, name='get_main_stock_analysis'),
    path('get_approved/', approved, name='approved'),
    path('get_approved_data/', get_approved_data, name='get_approved_data'),
    path('get_new_entries/', get_new_entries, name='get_new_entries'),
    path('get_new_entries_total/', get_new_entries_total, name='get_new_entries_total'),
    path('get_yearly_sales/', data_for_charts.get_yearly_sales, name='get_yearly_sales'),
    path('mark_as_read/', mark_as_read, name='mark_as_read'),
    path('approve/', approve, name='approve'),
    path('get_total_to_approve/', get_total_to_approve, name='get_total_to_approve'),
    path('edit_customer_data/<int:customer_id>', edit_customer_data, name='edit_customer_data'),
    path('delete_customer_data/', delete_customer_data, name='delete_customer_data'),
    path('total_rejected/', total_rejected, name='total_rejected'),
    path('get_rejected/', get_rejected, name='get_rejected'),
    # reseting user password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
]