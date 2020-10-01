from django.apps import AppConfig

default_app_config = 'home.apps.HomeConfig'

class HomeConfig(AppConfig):
    name = 'home'
    def ready(self):
        import main.signals
