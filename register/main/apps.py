from django.apps import AppConfig

default_app_config = 'main.apps.MainConfig'

class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals