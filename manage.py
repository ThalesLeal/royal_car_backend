#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royal_car_wash_backend.settings')
    
    # Interceptar comando runserver para desabilitar StatReloader por padrão
    if len(sys.argv) >= 2 and sys.argv[1] == 'runserver':
        # Se não foi especificado --reload, adicionar --noreload
        if '--reload' not in sys.argv and '--noreload' not in sys.argv:
            sys.argv.append('--noreload')
            print("🚀 Servidor iniciando em modo otimizado (sem StatReloader)")
            print("📝 Para usar StatReloader: python manage.py runserver --reload")
            print("⚡ Para modo otimizado: python manage.py runserver")
            print("-" * 50)
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
