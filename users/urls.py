from django.urls import path
from .apps import UsersConfig
from rest_framework.routers import DefaultRouter
from users import views

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('payments/', views.PaymentListAPIView.as_view(), name='payments'),
] + router.urls