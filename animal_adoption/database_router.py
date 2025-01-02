from django.conf import settings

class MasterSlaveRouter:
    """
    Rozdziela zapytania do bazy danych na podstawie operacji:
    - zapisy (insert, update, delete) idą do mastera
    - odczyty (select) idą do slave'a
    """
    def db_for_read(self, model, **hints):
        return 'replica' if 'replica' in settings.DATABASES else 'default'

    def db_for_write(self, model, **hints):
        """
        Zwraca 'default' (master) dla operacji zapisu.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Pozwala na relacje między bazami danych.
        """
        return True
