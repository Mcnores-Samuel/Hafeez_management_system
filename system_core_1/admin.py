from django.contrib import admin
from .adminsites.admin_mainstorage import MainStorageAdmin
from .adminsites.Admin_airtel_devices import Airtel_mifi_storageAdmin
from .adminsites.admin_user_profile import UserAdminModel
from .adminsites.admin_price_reference import PriceReferenceAdmin
from .adminsites.admin_agent_profile import AgentProfileAdmin
from .adminsites.admin_user_avatars import UserAvatarAdmin
from .adminsites.admin_employees import EmployeeAdmin
from .adminsites.admin_feedback import FeedbackAdmin
from .adminsites.admin_notification import NotificationsAdmin
from .adminsites.admin_commission import CommissionAdmin
from .adminsites.promoterPayments_admin import PromoterPaymentsAdmin
from .adminsites.admin_contacts import ContactAdmin
from .adminsites.admin_refarbished_phone import RefarbishedDevicesAdmin
from .models.agent_profile import AgentProfile
from .models.user_profile import UserProfile, UserAvatar
from .models.main_storage import MainStorage
from .models.user_profile import Employee
from .models.main_storage import Airtel_mifi_storage
from .models.feedback import Feedback
from .models.notifications import Notifications
from .models.commission import Commission
from .models.promoter_payments import PromoterPayments
from .models.contacts import Contact
from .models.refarbished_devices import RefarbishedDevices


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