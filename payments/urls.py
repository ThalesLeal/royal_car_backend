from django.urls import path
from . import views

urlpatterns = [
    # Payments
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('payments/stats/', views.payment_stats, name='payment-stats'),
    
    # Coupons
    path('coupons/', views.CouponListView.as_view(), name='coupon-list'),
    path('coupons/<int:pk>/', views.CouponDetailView.as_view(), name='coupon-detail'),
    path('coupons/validate/', views.validate_coupon, name='validate-coupon'),
    path('coupons/apply/<int:appointment_id>/', views.apply_coupon, name='apply-coupon'),
    
    # Coupon usage
    path('coupon-usage/', views.CouponUsageListView.as_view(), name='coupon-usage-list'),
]
