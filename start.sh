#!/bin/bash
# Script para iniciar o servidor Django sem StatReloader
# Uso: ./start.sh ou bash start.sh

echo "🚀 Iniciando Royal Car Wash Backend..."
echo "⚡ Modo otimizado - sem StatReloader"
echo "📝 Para parar: Ctrl+C"
echo "----------------------------------------"

# Desabilitar autoreload e iniciar servidor
DJANGO_AUTORELOAD=0 python manage.py runserver 127.0.0.1:8000 --noreload