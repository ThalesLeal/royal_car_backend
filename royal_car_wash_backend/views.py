from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_root(request):
    """API root endpoint with available endpoints"""
    endpoints = {
        "message": "Royal Car Wash API - Backend funcionando!",
        "version": "1.0.0",
        "endpoints": {
            "authentication": {
                "base_url": "/api/auth/",
                "endpoints": [
                    "GET /users/ - Listar usuários",
                    "POST /users/register/ - Cadastrar usuário", 
                    "POST /users/login/ - Fazer login",
                    "POST /users/logout/ - Fazer logout",
                    "GET /users/profile/ - Perfil do usuário",
                    "GET /content/ - Conteúdo do site"
                ]
            },
            "services": {
                "base_url": "/api/services/",
                "endpoints": [
                    "GET /services/ - Listar serviços",
                    "POST /services/ - Criar serviço (Admin)",
                    "GET /employees/ - Listar funcionários",
                    "GET /inventory/ - Listar estoque (Admin)",
                    "GET /expenses/ - Listar despesas (Admin)"
                ]
            },
            "appointments": {
                "base_url": "/api/appointments/",
                "endpoints": [
                    "GET /appointments/ - Listar agendamentos",
                    "POST /appointments/ - Criar agendamento",
                    "GET /time-slots/available/ - Obter horários disponíveis",
                    "GET /appointments/stats/ - Estatísticas de agendamentos",
                    "GET /chat-messages/ - Mensagens do chat"
                ]
            },
            "payments": {
                "base_url": "/api/payments/",
                "endpoints": [
                    "GET /payments/ - Listar pagamentos",
                    "POST /payments/ - Criar pagamento",
                    "GET /coupons/ - Listar cupons",
                    "POST /coupons/validate/ - Validar cupom",
                    "POST /coupons/apply/{id}/ - Aplicar cupom"
                ]
            },
            "loyalty": {
                "base_url": "/api/loyalty/",
                "endpoints": [
                    "GET /loyalty-points/ - Pontos de fidelidade",
                    "GET /loyalty-rewards/ - Recompensas disponíveis",
                    "GET /loyalty-status/ - Status de fidelidade",
                    "POST /loyalty-rewards/{id}/redeem/ - Resgatar recompensa"
                ]
            },
            "admin": {
                "base_url": "/admin/",
                "description": "Painel administrativo Django"
            }
        },
        "authentication": {
            "type": "Token Authentication",
            "header": "Authorization: Token <your-token>"
        }
    }
    return JsonResponse(endpoints, json_dumps_params={'indent': 2})
