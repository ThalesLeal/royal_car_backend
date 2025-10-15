# 🚀 Comandos do Servidor Django

## ⚡ Configuração Atual

O `manage.py` foi customizado para **desabilitar o StatReloader por padrão**, proporcionando melhor performance.

## 📝 Comandos Disponíveis

### 1. **Comando Padrão (Recomendado)**
```bash
python manage.py runserver
```
- ✅ **Sem StatReloader** (modo otimizado)
- ✅ **Inicialização rápida**
- ✅ **Menos uso de CPU**
- ✅ **Logs limpos**

### 2. **Com StatReloader (se necessário)**
```bash
python manage.py runserver --reload
```
- 🔄 **Com StatReloader** (recarregamento automático)
- 🐌 **Mais lento** na inicialização
- 📊 **Mais logs** no console
- 🔄 **Recarrega automaticamente** quando arquivos mudam

### 3. **Especificar Porta**
```bash
python manage.py runserver 8080
python manage.py runserver 127.0.0.1:8080
```

### 4. **Outros Comandos Úteis**
```bash
# Migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell interativo
python manage.py shell
```

## 🎯 Comportamento Atual

### Quando você executa `python manage.py runserver`:

1. **Detecta** que é o comando runserver
2. **Verifica** se não foi especificado --reload ou --noreload
3. **Adiciona automaticamente** --noreload
4. **Mostra mensagem** informativa
5. **Inicia servidor** em modo otimizado

### Mensagem que aparece:
```
🚀 Servidor iniciando em modo otimizado (sem StatReloader)
📝 Para usar StatReloader: python manage.py runserver --reload
⚡ Para modo otimizado: python manage.py runserver
--------------------------------------------------
```

## 🔧 Vantagens da Configuração

### ✅ **Modo Otimizado (Padrão):**
- **Inicialização rápida** (sem StatReloader)
- **Menos uso de CPU** (sem monitoramento de arquivos)
- **Logs limpos** (apenas informações importantes)
- **Ideal para desenvolvimento** quando você não precisa de recarregamento automático

### 🔄 **Modo com StatReloader (quando necessário):**
- **Recarregamento automático** quando arquivos mudam
- **Conveniente** para desenvolvimento ativo
- **Mais lento** na inicialização
- **Mais logs** no console

## 📊 Comparação

| Comando | StatReloader | Performance | Recarregamento | Uso |
|---------|--------------|-------------|----------------|-----|
| `python manage.py runserver` | ❌ | ⚡ Rápido | Manual | Padrão |
| `python manage.py runserver --reload` | ✅ | 🐌 Lento | Automático | Quando necessário |

## 🎉 Resultado

Agora você pode simplesmente executar:
```bash
python manage.py runserver
```

E o servidor vai rodar **automaticamente em modo otimizado** sem StatReloader! 🚀




