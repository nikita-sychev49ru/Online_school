from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserRegistrationSerializer, CreatePaymentSerializer
from users.services import PaymentSessionService


class UserRegistrationAPIView(generics.CreateAPIView):
    """контроллер для регистрации пользователя"""

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """вьюсет представлений для объектов модели пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = CreatePaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # получаем сумму оплаты из цены оплачиваемого курса или урока
            amount = 0
            if serializer.validated_data.get('paid_course'):
                amount = serializer.validated_data['paid_course'].price
            elif serializer.validated_data.get('paid_lesson'):
                amount = serializer.validated_data['paid_lesson'].price

            # собираем данные для создания продукта и цены в Stripe
            payment_data = {**serializer.validated_data, 'amount': amount}

            # создаем платеж через сервис
            payment = PaymentSessionService.create_payment_session(payment_data, request.user)
            # получаем новый объект платежа, содержащий id сессии в stripe и ссылку на оплату
            return Response(
                PaymentSerializer(payment, context={'request': request}).data, status=status.HTTP_201_CREATED
            )
        # либо получаем ошибку 400, если создать платеж не удалось
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    """представление для списка платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = [
        'payment_date',
    ]


class PaymentSuccessView(APIView):
    """Обработка успешной оплаты"""

    permission_classes = []

    def get(self, request):
        # обновить статус платежа на 'Оплачено'
        request.GET.get('session_id')
        return Response({'status': 'success', 'message': 'Оплата прошла успешно'})


class PaymentCancelView(APIView):
    """Обработка отмены оплаты"""

    permission_classes = []

    def get(self, request):
        # обновить статус платежа на 'Ошибка оплаты'
        request.GET.get('session_id')
        return Response({'status': 'cancelled', 'message': 'Оплата отменена'})
