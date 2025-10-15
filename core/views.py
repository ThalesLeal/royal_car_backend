from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .models import User, SiteContent
from .serializers import UserSerializer, UserLoginSerializer, SiteContentSerializer


class ListarCriarUsuariosView(generics.ListCreateAPIView):
    """Listar e criar usuários"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class DetalharUsuariosView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir usuário"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Usuários só podem acessar seu próprio perfil, exceto admins
        if self.request.user.is_admin:
            return super().get_object()
        return self.request.user

    def patch(self, request, *args, **kwargs):
        # Garantir atualização parcial ao receber PATCH
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def cadastrar_usuario(request):
    """Cadastro de usuário"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def fazer_login(request):
    """Login do usuário"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def fazer_logout(request):
    """Logout do usuário"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Falha no logout'}, status=status.HTTP_400_BAD_REQUEST)


class ListarConteudoSiteView(generics.ListAPIView):
    """Listar conteúdo do site"""
    queryset = SiteContent.objects.filter(is_active=True)
    serializer_class = SiteContentSerializer
    permission_classes = [permissions.AllowAny]


class DetalharConteudoSiteView(generics.RetrieveAPIView):
    """Detalhar conteúdo do site"""
    queryset = SiteContent.objects.filter(is_active=True)
    serializer_class = SiteContentSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def perfil_usuario(request):
    """Obter perfil do usuário atual"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)