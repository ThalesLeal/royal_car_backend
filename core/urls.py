from django.urls import path
from . import views

urlpatterns = [
    # Gerenciamento de usuários
    path('users/', views.ListarCriarUsuariosView.as_view(), name='listar-criar-usuarios'),
    path('users/<int:pk>/', views.DetalharUsuariosView.as_view(), name='detalhar-usuarios'),
    path('users/register/', views.cadastrar_usuario, name='cadastrar-usuario'),
    path('users/login/', views.fazer_login, name='fazer-login'),
    path('users/logout/', views.fazer_logout, name='fazer-logout'),
    path('users/profile/', views.perfil_usuario, name='perfil-usuario'),
    
    # Conteúdo do site
    path('content/', views.ListarConteudoSiteView.as_view(), name='listar-conteudo-site'),
    path('content/<int:pk>/', views.DetalharConteudoSiteView.as_view(), name='detalhar-conteudo-site'),
]
