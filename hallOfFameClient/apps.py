from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class HallOfFameClientConfig(AppConfig):
    name = 'hallOfFameClient'

    def ready(self):
        print("HAOFC ready")



