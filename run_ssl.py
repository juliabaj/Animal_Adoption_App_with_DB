import os
from django.core.management.base import BaseCommand
from subprocess import run
from django.conf import settings

class Command(BaseCommand):
    help = "Run Django development server with SSL"

    def handle(self, *args, **kwargs):
        # Ścieżki do certyfikatu i klucza
        cert = settings.BASE_DIR / 'localhost1.crt'
        key = settings.BASE_DIR / 'localhost1.key'

        if not cert.exists() or not key.exists():
            self.stdout.write(self.style.ERROR("Certyfikat lub klucz nie istnieją!"))
            return

        self.stdout.write(self.style.SUCCESS(f"Uruchamianie serwera SSL..."))
        # Uruchomienie serwera z certyfikatem
        run(["python", "manage.py", "runsslserver", "--certificate", str(cert), "--key", str(key)])
