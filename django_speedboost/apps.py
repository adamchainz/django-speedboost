from django.apps import AppConfig

import _django_speedboost

try:
    # Django 1.8+
    from django.db.backends.mysql.operations import DatabaseOperations
except ImportError:
    from django.db.backends.mysql.base import DatabaseOperations


class SpeedboostConfig(AppConfig):
    name = 'django_speedboost'
    verbose_name = 'Django Speedboost'

    def ready(self):
        # Monkey patch!
        self._orig_quote_name = DatabaseOperations.quote_name
        DatabaseOperations.quote_name = _django_speedboost.mysql_quote_name
