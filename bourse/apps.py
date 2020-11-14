from django.apps import AppConfig


class BourseConfig(AppConfig):
    name = 'bourse'

    def ready(self):
        from . import updater
        updater.start()
