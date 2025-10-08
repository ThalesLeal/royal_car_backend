from django.urls import path
from . import views

urlpatterns = [
    # Agendamentos
    path('appointments/', views.ListarCriarAgendamentosView.as_view(), name='listar-criar-agendamentos'),
    path('appointments/<int:pk>/', views.DetalharAgendamentosView.as_view(), name='detalhar-agendamentos'),
    path('appointments/stats/', views.estatisticas_agendamentos, name='estatisticas-agendamentos'),
    
    # Horários disponíveis
    path('time-slots/', views.ListarCriarHorariosDisponiveisView.as_view(), name='listar-criar-horarios-disponiveis'),
    path('time-slots/<int:pk>/', views.DetalharHorariosDisponiveisView.as_view(), name='detalhar-horarios-disponiveis'),
    path('time-slots/available/', views.obter_horarios_disponiveis, name='obter-horarios-disponiveis'),
    
    # Mensagens do chat
    path('chat-messages/', views.ListarCriarMensagensChatView.as_view(), name='listar-criar-mensagens-chat'),
    path('chat-messages/<int:pk>/', views.DetalharMensagensChatView.as_view(), name='detalhar-mensagens-chat'),
    path('chat-messages/<int:message_id>/read/', views.marcar_mensagem_lida, name='marcar-mensagem-lida'),
]
