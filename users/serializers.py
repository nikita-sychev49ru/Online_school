from rest_framework import serializers

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Платеж"""
    class Meta:
        model = Payment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователь"""
    # получаем список платежей пользователя
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'city', 'avatar', 'payments']