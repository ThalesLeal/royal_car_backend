from django.urls import path
from . import views

urlpatterns = [
    # Loyalty points
    path('loyalty-points/', views.LoyaltyPointsListView.as_view(), name='loyalty-points-list'),
    path('loyalty-points/<int:pk>/', views.LoyaltyPointsDetailView.as_view(), name='loyalty-points-detail'),
    path('loyalty-points/user/<int:user_id>/', views.LoyaltyPointsDetailView.as_view(), name='loyalty-points-user'),
    
    # Loyalty rewards
    path('loyalty-rewards/', views.LoyaltyRewardListView.as_view(), name='loyalty-reward-list'),
    path('loyalty-rewards/<int:pk>/', views.LoyaltyRewardDetailView.as_view(), name='loyalty-reward-detail'),
    path('loyalty-rewards/<int:reward_id>/redeem/', views.redeem_reward, name='redeem-reward'),
    
    # Loyalty transactions
    path('loyalty-transactions/', views.LoyaltyTransactionListView.as_view(), name='loyalty-transaction-list'),
    path('loyalty-transactions/user/<int:user_id>/', views.LoyaltyTransactionListView.as_view(), name='loyalty-transaction-user'),
    
    # Loyalty tiers
    path('loyalty-tiers/', views.LoyaltyTierListView.as_view(), name='loyalty-tier-list'),
    path('loyalty-tiers/<int:pk>/', views.LoyaltyTierDetailView.as_view(), name='loyalty-tier-detail'),
    
    # Loyalty status
    path('loyalty-status/', views.loyalty_status, name='loyalty-status'),
    path('loyalty-status/user/<int:user_id>/', views.loyalty_status, name='loyalty-status-user'),
    
    # Admin functions
    path('admin/add-points/<int:user_id>/', views.add_points, name='add-points'),
]
