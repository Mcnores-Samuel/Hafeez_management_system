from django.contrib import admin
from system_core_1.adminsites.admin_mainstorage import MainStorageAdmin
from system_core_1.adminsites.Admin_airtel_devices import Airtel_mifi_storageAdmin
from system_core_1.adminsites.admin_user_profile import UserAdminModel
from system_core_1.adminsites.admin_agent_profile import AgentProfileAdmin
from system_core_1.adminsites.admin_user_avatars import UserAvatarAdmin
from system_core_1.adminsites.admin_employees import EmployeeAdmin
from system_core_1.adminsites.admin_feedback import FeedbackAdmin
from system_core_1.adminsites.admin_notification import NotificationsAdmin
from system_core_1.adminsites.admin_commission import CommissionAdmin
from system_core_1.adminsites.promoterPayments_admin import PromoterPaymentsAdmin
from system_core_1.adminsites.admin_contacts import ContactAdmin
from system_core_1.adminsites.admin_refarbished_phone import RefarbishedDevicesAdmin, RefarbishedDevicesSalesAdmin
from system_core_1.adminsites.accessories import AdminAccessories, AdminAccessary_Sales
from system_core_1.adminsites.admin_expenses import ExpensesAdmin, FixedAssetsAdmin, CapitalAdmin, LiabilityAdmin
from system_core_1.adminsites.admin_appliances import AppliancesAdmin, Appliance_SalesAdmin
from system_core_1.models.agent_profile import AgentProfile
from system_core_1.models.user_profile import UserProfile, UserAvatar
from system_core_1.models.main_storage import MainStorage
from system_core_1.models.user_profile import Employee
from system_core_1.models.main_storage import Airtel_mifi_storage
from system_core_1.models.feedback import Feedback
from system_core_1.models.notifications import Notifications
from system_core_1.models.commission import Commission
from system_core_1.models.promoter_payments import PromoterPayments
from system_core_1.models.contacts import Contact
from system_core_1.models.refarbished_devices import RefarbishedDevices, RefarbishedDevicesSales
from system_core_1.models.accessories import Accessories, Accessory_Sales
from system_core_1.models.appliances import Appliances, Appliance_Sales
from system_core_1.models.expenses import Expenses, FixedAssets, Capital, Liability


admin.site.site_url = "/system_core_1/dashboard"
admin.site.site_header = "HAFEEZ MANAGEMENT SYSTEM"
admin.site.site_title = "Hafeez"
admin.site.index_title = "Hafeez Management"

admin.site.register(MainStorage, MainStorageAdmin)
admin.site.register(Airtel_mifi_storage, Airtel_mifi_storageAdmin)
admin.site.register(UserProfile, UserAdminModel)
admin.site.register(AgentProfile, AgentProfileAdmin)
admin.site.register(UserAvatar, UserAvatarAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(RefarbishedDevices, RefarbishedDevicesAdmin)
admin.site.register(PromoterPayments, PromoterPaymentsAdmin)
admin.site.register(Accessories, AdminAccessories)
admin.site.register(Accessory_Sales, AdminAccessary_Sales)
admin.site.register(Appliances, AppliancesAdmin)
admin.site.register(Appliance_Sales, Appliance_SalesAdmin)
admin.site.register(RefarbishedDevicesSales, RefarbishedDevicesSalesAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(FixedAssets, FixedAssetsAdmin)
admin.site.register(Capital, CapitalAdmin)
admin.site.register(Liability, LiabilityAdmin)