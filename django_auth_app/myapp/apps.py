from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_auth_app.myapp'

    def ready(self):
        # ✅ Automatically connect signals when app is ready
        import django_auth_app.myapp.signals
