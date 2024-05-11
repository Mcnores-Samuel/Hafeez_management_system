from django.contrib import admin
from .adminsites.admin_mainstorage import MainStorageAdmin
from .adminsites.Admin_airtel_devices import Airtel_mifi_storageAdmin
from .adminsites.admin_user_profile import UserAdminModel
from .adminsites.admin_customer_details import CustomerDataAdmin
from .adminsites.admin_customer_order import PhoneDataAdmin
from .adminsites.admin_price_reference import PriceReferenceAdmin
from .adminsites.admin_agent_profile import AgentProfileAdmin
from .adminsites.admin_user_avatars import UserAvatarAdmin
from .adminsites.admin_employees import EmployeeAdmin
from .adminsites.admin_special_orders import SpecialOrdersAdmin
from .adminsites.admin_feedback import FeedbackAdmin
from .adminsites.admin_notification import NotificationsAdmin
from .adminsites.admin_commission import CommissionAdmin
from .adminsites.admin_contacts import ContactAdmin
from .adminsites.admin_refarbished_phone import RefarbishedDevicesAdmin
from .adminsites.admin_account_manager import AccountManagerAdmin
from .models.special_orders import SpecialOrders
from .models.customer_details import CustomerData
from .models.agent_profile import AgentProfile
from .models.customer_order import PhoneData
from .models.user_profile import UserProfile, UserAvatar
from .models.main_storage import MainStorage
from .models.reference import Price_reference
from .models.user_profile import Employee
from .models.main_storage import Airtel_mifi_storage
from .models.feedback import Feedback
from .models.notifications import Notifications
from .models.commission import Commission
from .models.contacts import Contact
from .models.refarbished_devices import RefarbishedDevices
from .models.account_manager import AccountManager
from .models.prices import (YellowPrices, MosesPrices, ChrisMZPrices,
                            Chris25Prices, BuzzMchinjiPrices)
from .adminsites.admin_prices import (AdminYellowPrices, AdminMosesPrices,
                                      AdminChrisMZPrices, AdminChris25Prices,
                                      AdminBuzzMchinjiPrices)


admin.site.site_url = "/system_core_1/dashboard"
admin.site.site_header = "HAFEEZ MANAGEMENT SYSTEM"
admin.site.site_title = "Hafeez"
admin.site.index_title = "Hafeez Management"

admin.site.register(MainStorage, MainStorageAdmin)
admin.site.register(Airtel_mifi_storage, Airtel_mifi_storageAdmin)
admin.site.register(UserProfile, UserAdminModel)
admin.site.register(CustomerData, CustomerDataAdmin)
admin.site.register(PhoneData, PhoneDataAdmin)
admin.site.register(Price_reference, PriceReferenceAdmin)
admin.site.register(AgentProfile, AgentProfileAdmin)
admin.site.register(UserAvatar, UserAvatarAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(SpecialOrders, SpecialOrdersAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(YellowPrices, AdminYellowPrices)
admin.site.register(MosesPrices, AdminMosesPrices)
admin.site.register(ChrisMZPrices, AdminChrisMZPrices)
admin.site.register(Chris25Prices, AdminChris25Prices)
admin.site.register(BuzzMchinjiPrices, AdminBuzzMchinjiPrices)
admin.site.register(RefarbishedDevices, RefarbishedDevicesAdmin)
admin.site.register(AccountManager, AccountManagerAdmin)