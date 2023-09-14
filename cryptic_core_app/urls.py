from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .view_modules import registration_view, data_updates

urlpatterns =[
    path('', views.home_page, name='home_page'),
    path('sign_up/', registration_view.sign_up, name='sign_up'),
    path('sign_in/', registration_view.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', data_updates.profile, name='profile'),
    path('change_password/', data_updates.change_password, name='change_password'),
    path('combinedData_collection/<int:data_id>/', views.combinedData_collection, name='combinedData_collection'),
    path('add_contract_number/', data_updates.add_contract_number, name='add_contract_number'),
    path('in_stock/', data_updates.in_stock, name='in_stock'),
    path('stock_out/', data_updates.stock_out, name='stock_out'),
    # reseting user password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
]