from django.apps import AppConfig


class DecorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "decor"

    def ready(self):
        # Khi app khởi động, import signals để đăng ký
        import decor.signals
