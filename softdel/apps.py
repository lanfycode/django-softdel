from django.apps import AppConfig
from django.db import DEFAULT_DB_ALIAS
from django.db.models.signals import post_migrate, pre_migrate


def handle_pre_migrate(app_config, using=DEFAULT_DB_ALIAS, **kwargs):
    pass


def handle_post_migrate(app_config, using=DEFAULT_DB_ALIAS, **kwargs):
    pass


class SoftDelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'softdel'

    def ready(self):
        pre_migrate.connect(handle_pre_migrate)
        post_migrate.connect(handle_post_migrate)
