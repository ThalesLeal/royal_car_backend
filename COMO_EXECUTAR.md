# 🚀 Como Executar o Servidor Django

## ⚡ Opções de Execução (Sem StatReloader)

### 1. **Comando Direto (Recomendado)**
```bash
python manage.py runserver 127.0.0.1:8000 --noreload
```

### 2. **Script Automatizado**
```bash
./start.sh
```

### 3. **Script Python Avançado**
```bash
python runserver_fast.py
```

## 🔧 Diferenças das Opções

| Método | StatReloader | Performance | Recarregamento |
|--------|--------------|-------------|----------------|
| `--noreload` | ❌ Desabilitado | ⚡ Rápido | Manual |
| `./start.sh` | ❌ Desabilitado | ⚡ Rápido | Manual |
| `runserver_fast.py` | ❌ Desabilitado | ⚡ Rápido | Manual |
| `python manage.py runserver` | ✅ Habilitado | 🐌 Lento | Automático |

## 📝 Comandos Úteis

### Parar o servidor:
```bash
# Ctrl+C no terminal onde está rodando
# OU
pkill -f "python manage.py runserver"
```

### Verificar se está rodando:
```bash
curl http://localhost:8000/api/
```

### Logs do servidor:
```bash
# O servidor mostra apenas warnings e erros
# Para ver todos os logs, use:
python manage.py runserver --verbosity=2
```

## ⚙️ Configurações de Otimização Aplicadas

- ✅ **StatReloader desabilitado** - Sem monitoramento de arquivos
- ✅ **Logging otimizado** - Apenas warnings e erros
- ✅ **Debug de templates desabilitado** - Melhor performance
- ✅ **Timezone otimizado** - Configuração eficiente

## 🎯 Resultado

- **Inicialização mais rápida** (sem StatReloader)
- **Menos uso de CPU** (sem monitoramento contínuo)
- **Logs mais limpos** (apenas informações importantes)
- **Performance melhorada** em desenvolvimento

## 🔄 Para Recarregar Mudanças

Como o StatReloader está desabilitado, você precisa:

1. **Parar o servidor**: `Ctrl+C`
2. **Iniciar novamente**: `python manage.py runserver 127.0.0.1:8000 --noreload`

Ou use o script: `./start.sh`
