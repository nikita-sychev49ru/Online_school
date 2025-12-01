from rest_framework import serializers

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Платеж"""

    link = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        read_only_fields = ['public_id', 'status', 'payment_date', 'paid_date', 'stripe_session_id', 'link']
        fields = '__all__'

    def get_link(self, obj):
        """Генерирует URL для оплаты через Stripe Checkout"""
        if obj.stripe_session_id:
            return f"https://checkout.stripe.com/pay/{obj.stripe_session_id}"
        return None


class CreatePaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания платежа"""

    link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = ['paid_course', 'paid_lesson', 'payment_method', 'link']
        read_only_fields = ['link']

    def validate(self, data):
        """Проверяем, что в теле POST-запроса указан курс или урок, который хотим оплатить"""
        if not data.get('paid_course') and not data.get('paid_lesson'):
            raise serializers.ValidationError('Должен быть указан курс или урок')
        if data.get('paid_course') and data.get('paid_lesson'):
            raise serializers.ValidationError('Можно указать только курс или только урок')
        return data

    def get_link(self, obj):
        """Генерирует URL для оплаты через Stripe Checkout"""
        if obj.stripe_session_id:
            return f"https://checkout.stripe.com/pay/{obj.stripe_session_id}"
        return None


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации"""

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями"""

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'city', 'avatar', 'payments']
