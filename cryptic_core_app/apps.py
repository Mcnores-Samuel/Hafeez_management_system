from django.apps import AppConfig
from cryptic_core_app.helper_modules.agent_code import generate_and_store_special_code
import threading


class CrypticCoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cryptic_core_app'

    def ready(self):
        thread = threading.Thread(target=generate_and_store_special_code)
        thread.setDaemon(True)
        thread.start()
