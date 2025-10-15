from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import LoyaltyPoints, LoyaltyReward, LoyaltyTransaction, LoyaltyTier
from .serializers import (
    LoyaltyPointsSerializer, LoyaltyRewardSerializer, LoyaltyTransactionSerializer,
    LoyaltyTierSerializer, LoyaltyStatusSerializer
)


class LoyaltyPointsListView(generics.ListAPIView):
    """List loyalty points"""
    queryset = LoyaltyPoints.objects.all()
    serializer_class = LoyaltyPointsSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['total_points', 'created_at']
    ordering = ['-total_points']


class LoyaltyPointsDetailView(generics.RetrieveAPIView):
    """Retrieve loyalty points for a user"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if self.request.user.is_admin and 'user_id' in self.kwargs:
            user_id = self.kwargs['user_id']
            try:
                from core.models import User
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return None
        
        points, created = LoyaltyPoints.objects.get_or_create(user=user)
        return points


class LoyaltyRewardListView(generics.ListCreateAPIView):
    """List and create loyalty rewards"""
    queryset = LoyaltyReward.objects.filter(is_active=True)
    serializer_class = LoyaltyRewardSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['reward_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['points_required', 'created_at']
    ordering = ['points_required']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class LoyaltyRewardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a loyalty reward"""
    queryset = LoyaltyReward.objects.all()
    serializer_class = LoyaltyRewardSerializer
    permission_classes = [permissions.IsAdminUser]


class LoyaltyTransactionListView(generics.ListAPIView):
    """List loyalty transactions"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoyaltyTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'user', 'appointment']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin and 'user_id' in self.kwargs:
            user_id = self.kwargs['user_id']
            try:
                from core.models import User
                target_user = User.objects.get(id=user_id)
                return LoyaltyTransaction.objects.filter(user=target_user)
            except User.DoesNotExist:
                return LoyaltyTransaction.objects.none()
        return LoyaltyTransaction.objects.filter(user=user)


class LoyaltyTierListView(generics.ListCreateAPIView):
    """List and create loyalty tiers"""
    queryset = LoyaltyTier.objects.filter(is_active=True)
    serializer_class = LoyaltyTierSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['min_points', 'created_at']
    ordering = ['min_points']


class LoyaltyTierDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a loyalty tier"""
    queryset = LoyaltyTier.objects.all()
    serializer_class = LoyaltyTierSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def loyalty_status(request):
    """Get user's loyalty status"""
    user = request.user
    if request.user.is_admin and 'user_id' in request.GET:
        user_id = request.GET['user_id']
        try:
            from core.models import User
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get or create loyalty points
    points, created = LoyaltyPoints.objects.get_or_create(user=user)
    
    # Get current tier
    current_tier = None
    next_tier = None
    points_to_next = None
    
    tiers = LoyaltyTier.objects.filter(is_active=True).order_by('min_points')
    for tier in tiers:
        if tier.is_eligible(points.total_points):
            current_tier = tier
        elif not current_tier and tier.min_points > points.total_points:
            next_tier = tier
            points_to_next = tier.min_points - points.total_points
            break
    
    # Get available rewards
    available_rewards = LoyaltyReward.objects.filter(
        is_active=True,
        points_required__lte=points.available_points
    ).order_by('points_required')
    
    status_data = {
        'total_points': points.total_points,
        'available_points': points.available_points,
        'current_tier': LoyaltyTierSerializer(current_tier).data if current_tier else None,
        'next_tier': LoyaltyTierSerializer(next_tier).data if next_tier else None,
        'points_to_next_tier': points_to_next,
        'available_rewards': LoyaltyRewardSerializer(available_rewards, many=True).data
    }
    
    serializer = LoyaltyStatusSerializer(status_data)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def redeem_reward(request, reward_id):
    """Redeem a loyalty reward"""
    try:
        reward = LoyaltyReward.objects.get(id=reward_id, is_active=True)
        user = request.user
        
        # Get user's loyalty points
        points, created = LoyaltyPoints.objects.get_or_create(user=user)
        
        # Check if user has enough points
        if points.available_points < reward.points_required:
            return Response(
                {'error': 'Insufficient points'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get appointment ID if provided
        appointment_id = request.data.get('appointment_id')
        appointment = None
        if appointment_id:
            try:
                from agendamentos.models import Appointment
                appointment = Appointment.objects.get(id=appointment_id, customer=user)
            except Appointment.DoesNotExist:
                return Response(
                    {'error': 'Appointment not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Redeem points
        success = points.redeem_points(
            reward.points_required, 
            f"Resgate: {reward.name}"
        )
        
        if success:
            # Create transaction record
            LoyaltyTransaction.objects.create(
                user=user,
                points=-reward.points_required,
                transaction_type='redeemed',
                reason=f"Resgate: {reward.name}",
                appointment=appointment,
                reward=reward
            )
            
            return Response({
                'message': 'Reward redeemed successfully',
                'remaining_points': points.available_points
            })
        else:
            return Response(
                {'error': 'Failed to redeem reward'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except LoyaltyReward.DoesNotExist:
        return Response(
            {'error': 'Reward not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_points(request, user_id):
    """Add points to a user's account (admin only)"""
    try:
        from core.models import User
        user = User.objects.get(id=user_id)
        points_amount = request.data.get('points', 0)
        reason = request.data.get('reason', 'Pontos adicionados pelo admin')
        
        if points_amount <= 0:
            return Response(
                {'error': 'Points amount must be positive'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create loyalty points
        points, created = LoyaltyPoints.objects.get_or_create(user=user)
        points.add_points(points_amount, reason)
        
        return Response({
            'message': f'Added {points_amount} points to {user.first_name}',
            'total_points': points.total_points,
            'available_points': points.available_points
        })
        
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )