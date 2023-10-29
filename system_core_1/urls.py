from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (registration_view, data_updates, customer_registrar,
                    central_display, home_page, user_dashboard, action_on_data_select)


urlpatterns =[
    path('', home_page.home_page, name='home_page'),
    path('products/', home_page.products, name='products'),
    path('about/', home_page.about, name='about'),
    path('faq/', home_page.faq, name='faq'),
    path('terms/', home_page.terms, name='terms'),
    path('contact/', home_page.contact, name='contact'),
    path('services/', home_page.services, name='services'),
    path('privacy/', home_page.privacy, name='privacy'),
    path('sign_up/', registration_view.sign_up, name='sign_up'),
    path('resend_confirmation_email', registration_view.resend_confirmation_email, name='resend_confirmation_email'),
    path('generate_agent_code/', user_dashboard.generate_agent_code, name='generate_agent_code'),
    path('sign_in/', registration_view.sign_in, name='sign_in'),
    path('sign_out/', registration_view.sign_out, name='sign_out'),
    path('dashboard/', user_dashboard.dashboard, name='dashboard'),
    path('profile/', data_updates.profile, name='profile'),
    path('change_password/', data_updates.change_password, name='change_password'),
    path('combinedData_collection/<int:data_id>/', customer_registrar.combinedData_collection, name='combinedData_collection'),
    path('add_contract_number/', data_updates.add_contract_number, name='add_contract_number'),
    path('in_stock/', data_updates.in_stock, name='in_stock'),
    path('stock_out/', data_updates.stock_out, name='stock_out'),
    path('users/', central_display.users, name='users'),
    path('main_storage/', central_display.main_storage, name='main_storage'),
    path('agents_and_data/', central_display.agents_and_data, name='agents_and_data'),
    path('my_customers/', central_display.my_customers, name='my_customers'),
    path('action_on_click/<int:data_id>/', action_on_data_select.action_on_click, name='action_on_click'),
    # reseting user password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
]