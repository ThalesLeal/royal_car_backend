# 🚀 Royal Car Wash - Backend API

## 📁 Estrutura do Projeto

Este é o **backend** do projeto Royal Car Wash, desenvolvido em Django REST Framework.

### ⚠️ **IMPORTANTE - Separação Frontend/Backend**

- **Backend** (este diretório): Django + Python
- **Frontend** (diretório separado): React/Vue/Angular + Node.js

### 🚫 **O que NÃO deve estar aqui:**
- ❌ `node_modules/`
- ❌ `package-lock.json`
- ❌ Dependências do Node.js
- ❌ Código frontend (React, Vue, etc.)

### ✅ **O que DEVE estar aqui:**
- ✅ `manage.py`
- ✅ `requirements.txt`
- ✅ Apps Django (`core/`, `services/`, `appointments/`, etc.)
- ✅ `venv/` (ambiente virtual Python)

## 🛠️ Como Executar

### 1. **Ativar ambiente virtual:**
```bash
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

### 3. **Executar migrações:**
```bash
python manage.py migrate
```

### 4. **Iniciar servidor:**
```bash
# Opção 1 - Rápido (sem StatReloader)
python manage.py runserver 127.0.0.1:8000 --noreload

# Opção 2 - Script automatizado
./start.sh

# Opção 3 - Com npm (se configurado)
npm start
```

## 🌐 Endpoints da API

- **Base URL**: `http://localhost:8000/api/`
- **Documentação**: `http://localhost:8000/api/` (API Root)
- **Admin**: `http://localhost:8000/admin/`

### Principais Endpoints:
- `GET /api/` - Lista todos os endpoints
- `POST /api/auth/users/register/` - Cadastrar usuário
- `POST /api/auth/users/login/` - Fazer login
- `GET /api/services/` - Listar serviços
- `GET /api/appointments/` - Listar agendamentos
- `GET /api/payments/` - Listar pagamentos

## 🔧 Configurações

### Variáveis de Ambiente:
Crie um arquivo `.env` baseado no `env.example`:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DB_NAME=royal_car_wash_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### Banco de Dados:
- **Desenvolvimento**: SQLite (padrão)
- **Produção**: PostgreSQL (configurável)

## 📦 Dependências Python

```
Django==4.2.25
djangorestframework==3.16.1
django-cors-headers==4.9.0
python-decouple==3.8
Pillow==11.3.0
django-filter==24.2
```

## 🚀 Scripts Disponíveis

```bash
# Iniciar servidor otimizado
npm start

# Iniciar servidor com reload
npm run dev

# Executar migrações
npm run migrate

# Coletar arquivos estáticos
npm run collectstatic
```

## 🔍 Troubleshooting

### Problema: "Could not resolve @floating-ui"
**Solução**: Essas dependências são do frontend, não do backend. Remova `node_modules/` e `package-lock.json` do backend.

### Problema: Servidor lento
**Solução**: Use `--noreload` para desabilitar o StatReloader.

### Problema: CORS errors
**Solução**: Verifique se o frontend está rodando na porta configurada em `CORS_ALLOWED_ORIGINS`.

## 📝 Notas Importantes

1. **Este é apenas o backend** - O frontend deve estar em um diretório separado
2. **Não instale dependências Node.js aqui** - Use apenas Python/Django
3. **Use o ambiente virtual** - Sempre ative o `venv` antes de trabalhar
4. **Mantenha o .gitignore atualizado** - Para não commitar arquivos desnecessários




