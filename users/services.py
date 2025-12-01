import stripe
from config.settings import STRIPE_SECRET_KEY, STRIPE_SUCCESS_URL, STRIPE_CANCEL_URL

stripe.api_key = STRIPE_SECRET_KEY


class PaymentSessionService:
    """Сервис для работы с платежными сессиями Stripe"""

    @staticmethod
    def create_product_for_item(item):
        """Создание продукта в Stripe для курса или урока"""
        if hasattr(item, 'title'):
            product_data = {
                'name': item.title,
            }
        else:
            product_data = {'name': f'Item {item.id}'}

        return stripe.Product.create(**product_data)

    @staticmethod
    def create_price(amount, currency='rub', product_id=None):
        """Создание цены в Stripe"""
        return stripe.Price.create(
            unit_amount=int(amount * 100),  # Конвертируем в копейки/центы
            currency=currency,
            product=product_id,
        )

    @staticmethod
    def create_checkout_session(payment):
        """Создание сессии оплаты в Stripe"""
        # Определяем оплачиваемый item
        item = payment.paid_course if payment.paid_course else payment.paid_lesson

        # Создаем продукт
        product = PaymentSessionService.create_product_for_item(item)

        # Создаем цену
        price = PaymentSessionService.create_price(amount=payment.amount, currency='rub', product_id=product.id)

        # Создаем сессию оплаты
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=STRIPE_SUCCESS_URL,
            cancel_url=STRIPE_CANCEL_URL,
            client_reference_id=str(payment.public_id),
            metadata={
                'payment_id': str(payment.public_id),
                'user_id': str(payment.user.id),
                'item_type': 'course' if payment.paid_course else 'lesson',
                'item_id': str(item.id),
            },
        )

        return checkout_session

    @staticmethod
    def create_payment_session(payment_data, user):
        """Создание платежа и сессии оплаты"""
        from .models import Payment

        # Создаем объект платежа
        payment = Payment.objects.create(
            user=user,
            paid_course=payment_data.get('paid_course'),
            paid_lesson=payment_data.get('paid_lesson'),
            amount=payment_data.get('amount', 0),
            payment_method=payment_data.get('payment_method', Payment.STRIPE),
        )

        # Если это онлайн-оплата через Stripe
        if payment.payment_method == Payment.STRIPE:
            checkout_session = PaymentSessionService.create_checkout_session(payment)
            payment.stripe_session_id = checkout_session.id
            payment.save()

        return payment
