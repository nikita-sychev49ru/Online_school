from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer

class UserViewSet(viewsets.ModelViewSet):
    """вьюсет представлений для объектов модели пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PaymentListAPIView(generics.ListAPIView):
    """представление для списка платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date',]