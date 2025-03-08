from django.urls import path
from system_core_1.views.data_input import dispatch
from system_core_1.views.data_input import sales_register
from system_core_1.views.data_input import stock_taking
from system_core_1.views.data_input import recordairteldevices_payment
from system_core_1.views.data_input import feedback
from system_core_1.views.data_input import add_stock


urlpatterns = [
    #urls for adding stock and other data inputs
    path('add_to_stock/', add_stock.add_to_stock, name='add_to_stock'),
    path('add_accessaries/', add_stock.add_accessaries, name='add_accessaries'),
    path('add_appliances/', add_stock.add_appliances, name='add_appliances'),
    path('add_refarbished/', add_stock.add_refarbished, name='add_refarbished'),
    path('dispatch_stock/', dispatch.dispatch_stock, name='dispatch_stock'),
    path('uploadBulkSales/', sales_register.uploadBulkSales, name='uploadBulkSales'),
    path('accessary_sales', sales_register.accessary_sales, name='accessary_sales'),
    path('appliance_sales', sales_register.appliance_sales, name='appliance_sales'),
    path('refarbished_sales', sales_register.refarbished_sales, name='refarbished_sales'),
    path('combinedData_collection/<int:data_id>/', sales_register.combinedData_collection, name='combinedData_collection'),
    path('stock_taking/', stock_taking.stock_taking, name='stock_taking'),
    path('feedback/', feedback.feedback, name='feedback'),
]
