from django.apps import AppConfig


class LeaveManagementAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave_management_app'

    def ready(self):
        import leave_management_app.signals