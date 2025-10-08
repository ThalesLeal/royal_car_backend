#!/usr/bin/env python
"""
Script personalizado para rodar o servidor Django sem StatReloader
Para melhor performance em desenvolvimento
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.core.servers.basehttp import run
from django.core.wsgi import get_wsgi_application

def main():
    """Executa o servidor Django sem autoreload"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royal_car_wash_backend.settings')
    
    # Configurar Django
    django.setup()
    
    # Desabilitar autoreload
    os.environ['DJANGO_AUTORELOAD'] = '0'
    
    # Configurações do servidor
    host = '127.0.0.1'
    port = 8000
    
    print(f"🚀 Servidor Django iniciando em http://{host}:{port}")
    print("⚡ Modo otimizado - sem StatReloader")
    print("📝 Para parar: Ctrl+C")
    print("-" * 50)
    
    # Executar servidor
    try:
        from django.core.management.commands.runserver import Command
        command = Command()
        command.handle(
            addrport=f"{host}:{port}",
            use_reloader=False,  # Desabilita o StatReloader
            use_threading=True,
            verbosity=1
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
