import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY

def create_stripe_product(product_data):
    """Создает продукт в Stripe по полям 'name' и 'description'"""

    return stripe.Product.create(
        name=product_data["name"],
        description=product_data.get("description", "")
    )

def create_stripe_price(amount, product):
    """Создает цену в Stripe в рублях (в копейках) по полю id созданного продукта"""

    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=product.id,
    )

def create_stripe_sessions(price):
    """Создает сессию оплаты в Stripe. Возвращает кортеж с id сессии и ссылкой на оплату"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        cancel_url="http://127.0.0.1:8000/",
        line_items=[{
            "price": price.id,
            "quantity": 1,
        }],
        mode="payment",
    )
    return session.id, session.url
