from django.apps import AppConfig


class SystemCore1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'system_core_1'
    models = 'system_core_1.models'
