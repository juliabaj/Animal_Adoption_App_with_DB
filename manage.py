#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animal_adoption.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Ścieżki do certyfikatów znajdujących się w głównym katalogu projektu
    BASE_DIR = Path(__file__).resolve().parent
    cert = BASE_DIR / 'localhost1.crt'
    key = BASE_DIR / 'localhost1.key'

    # Automatyczne użycie runsslserver, jeśli użytkownik wpisze runserver
    if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
        sys.argv[1] = "runsslserver"
        sys.argv.extend(["--certificate", str(cert), "--key", str(key)])

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
