from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news_app"

    def ready(self):
        import news_app.signals
