# Royal Car Wash - Backend API

Backend Django REST API para o sistema de lavagem de carros Royal Car Wash.

## 🚀 Funcionalidades

### Autenticação e Usuários
- Sistema de autenticação com tokens
- Diferentes tipos de usuários (Cliente, Funcionário, Admin)
- Gerenciamento de perfis de usuário

### Serviços
- Cadastro e gerenciamento de serviços de lavagem
- Preços diferenciados por tipo de veículo
- Categorização de serviços (Lavagem, Enceramento, Detalhamento, Premium)

### Agendamentos
- Sistema completo de agendamentos
- Horários disponíveis por dia da semana
- Status de agendamento (Agendado, Confirmado, Em Andamento, Concluído, Cancelado)
- Sistema de chat entre cliente e equipe

### Pagamentos
- Múltiplas formas de pagamento (PIX, Cartão, Dinheiro)
- Sistema de cupons de desconto
- Controle de status de pagamento

### Fidelidade
- Programa de pontos de fidelidade
- Níveis de fidelidade com benefícios
- Recompensas resgatáveis
- Histórico de transações

### Administração
- Painel administrativo completo
- Relatórios e estatísticas
- Gerenciamento de estoque
- Controle de despesas

## 🛠️ Tecnologias

- **Django 4.2.25** - Framework web
- **Django REST Framework 3.16.1** - API REST
- **Django CORS Headers** - CORS para frontend
- **Django Filter** - Filtros avançados
- **Pillow** - Processamento de imagens
- **Python Decouple** - Gerenciamento de configurações

## 📦 Instalação

### Pré-requisitos
- Python 3.9+
- pip

### Configuração

1. **Clone o repositório**
```bash
git clone <repository-url>
cd royal_car_wash_backend
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor**
```bash
python manage.py runserver
```

## 📚 API Endpoints

### Autenticação (`/api/auth/`)
- `POST /users/register/` - Registro de usuário
- `POST /users/login/` - Login
- `POST /users/logout/` - Logout
- `GET /users/profile/` - Perfil do usuário
- `GET /content/` - Conteúdo do site

### Serviços (`/api/services/`)
- `GET /services/` - Listar serviços
- `POST /services/` - Criar serviço (Admin)
- `GET /services/{id}/` - Detalhes do serviço
- `GET /employees/` - Listar funcionários
- `GET /inventory/` - Listar estoque (Admin)
- `GET /expenses/` - Listar despesas (Admin)

### Agendamentos (`/api/appointments/`)
- `GET /appointments/` - Listar agendamentos
- `POST /appointments/` - Criar agendamento
- `GET /appointments/{id}/` - Detalhes do agendamento
- `GET /time-slots/available/` - Horários disponíveis
- `GET /appointments/stats/` - Estatísticas
- `GET /chat-messages/` - Mensagens do chat

### Pagamentos (`/api/payments/`)
- `GET /payments/` - Listar pagamentos
- `POST /payments/` - Criar pagamento
- `GET /coupons/` - Listar cupons
- `POST /coupons/validate/` - Validar cupom
- `POST /coupons/apply/{appointment_id}/` - Aplicar cupom

### Fidelidade (`/api/loyalty/`)
- `GET /loyalty-points/` - Pontos de fidelidade
- `GET /loyalty-rewards/` - Recompensas disponíveis
- `GET /loyalty-status/` - Status de fidelidade
- `POST /loyalty-rewards/{id}/redeem/` - Resgatar recompensa

## 🔐 Autenticação

A API utiliza autenticação por token. Para acessar endpoints protegidos:

1. Faça login em `/api/auth/users/login/`
2. Use o token retornado no header `Authorization: Token <seu-token>`

## 📊 Modelos de Dados

### User (Usuário)
- Informações básicas do usuário
- Tipos: Cliente, Funcionário, Admin
- Dados de contato e endereço

### Service (Serviço)
- Nome, descrição e categoria
- Duração em minutos
- Preços por tipo de veículo

### Appointment (Agendamento)
- Cliente, serviço e funcionário
- Data, hora e veículo
- Status e avaliação

### Payment (Pagamento)
- Método de pagamento
- Status e valor
- Dados da transação

### LoyaltyPoints (Pontos de Fidelidade)
- Pontos totais e disponíveis
- Histórico de transações
- Níveis de fidelidade

## 🚀 Deploy

### Variáveis de Ambiente para Produção
```env
SECRET_KEY=sua-secret-key-segura
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgresql://user:password@host:port/database
```

### Comandos de Deploy
```bash
python manage.py collectstatic
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte, entre em contato através do email: suporte@royalcarwash.com
# royal_car_backend
