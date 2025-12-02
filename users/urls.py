from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .apps import UsersConfig
from rest_framework.routers import DefaultRouter
from users import views

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('payments/', views.PaymentListAPIView.as_view(), name='payments'),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment-success'),
    path('payment/cancel/', views.PaymentCancelView.as_view(), name='payment-cancel'),
    path('payment_create/', views.PaymentCreateAPIView.as_view(), name='new_payment'),
    path('payment/<int:pk>/', views.PaymentRetrieveAPIView.as_view(), name='payment'),
] + router.urls
