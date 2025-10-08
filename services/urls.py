from django.urls import path
from . import views

urlpatterns = [
    # Serviços
    path('services/', views.ListarCriarServicosView.as_view(), name='listar-criar-servicos'),
    path('services/<int:pk>/', views.DetalharServicosView.as_view(), name='detalhar-servicos'),
    
    # Preços de serviços
    path('service-prices/', views.ListarCriarPrecosServicosView.as_view(), name='listar-criar-precos-servicos'),
    path('service-prices/<int:pk>/', views.DetalharPrecosServicosView.as_view(), name='detalhar-precos-servicos'),
    
    # Funcionários
    path('employees/', views.ListarCriarFuncionariosView.as_view(), name='listar-criar-funcionarios'),
    path('employees/<int:pk>/', views.DetalharFuncionariosView.as_view(), name='detalhar-funcionarios'),
    
    # Estoque
    path('inventory/', views.ListarCriarEstoqueView.as_view(), name='listar-criar-estoque'),
    path('inventory/<int:pk>/', views.DetalharEstoqueView.as_view(), name='detalhar-estoque'),
    
    # Despesas
    path('expenses/', views.ListarCriarDespesasView.as_view(), name='listar-criar-despesas'),
    path('expenses/<int:pk>/', views.DetalharDespesasView.as_view(), name='detalhar-despesas'),
]
