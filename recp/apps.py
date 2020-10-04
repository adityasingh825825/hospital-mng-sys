from django.apps import AppConfig


class RecpConfig(AppConfig):
    name = 'recp'
    
    def ready(self):
        import recp.signals
