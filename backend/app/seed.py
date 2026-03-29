import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select

from app.database import async_session
from app.models import Base, GiftCard, Product

PRODUCTS = [
    {
        "name": "Steam Gift Card $50",
        "category": "gaming",
        "price": Decimal("50.00"),
        "description": "Пополнение кошелька Steam на $50. Подходит для покупки игр, DLC и внутриигровых предметов.",
        "image_url": "https://placehold.co/400x300/1b2838/ffffff?text=Steam+$50",
    },
    {
        "name": "Steam Gift Card $100",
        "category": "gaming",
        "price": Decimal("100.00"),
        "description": "Пополнение кошелька Steam на $100.",
        "image_url": "https://placehold.co/400x300/1b2838/ffffff?text=Steam+$100",
    },
    {
        "name": "PlayStation Store $25",
        "category": "gaming",
        "price": Decimal("25.00"),
        "description": "Подарочная карта PlayStation Store. Покупайте игры, фильмы и подписки.",
        "image_url": "https://placehold.co/400x300/003087/ffffff?text=PS+Store+$25",
    },
    {
        "name": "PlayStation Store $50",
        "category": "gaming",
        "price": Decimal("50.00"),
        "description": "Подарочная карта PlayStation Store на $50.",
        "image_url": "https://placehold.co/400x300/003087/ffffff?text=PS+Store+$50",
    },
    {
        "name": "Xbox Game Pass Ultimate 1 Month",
        "category": "gaming",
        "price": Decimal("14.99"),
        "description": "Месячная подписка Xbox Game Pass Ultimate. Доступ к сотням игр на Xbox и PC.",
        "image_url": "https://placehold.co/400x300/107c10/ffffff?text=Xbox+GP",
    },
    {
        "name": "Nintendo eShop $35",
        "category": "gaming",
        "price": Decimal("35.00"),
        "description": "Подарочная карта Nintendo eShop для покупки игр на Switch.",
        "image_url": "https://placehold.co/400x300/e60012/ffffff?text=Nintendo+$35",
    },
    {
        "name": "Netflix Gift Card $30",
        "category": "entertainment",
        "price": Decimal("30.00"),
        "description": "Подарочная карта Netflix. Оплачивайте подписку без привязки банковской карты.",
        "image_url": "https://placehold.co/400x300/e50914/ffffff?text=Netflix+$30",
    },
    {
        "name": "Spotify Premium 3 Months",
        "category": "entertainment",
        "price": Decimal("29.99"),
        "description": "3 месяца подписки Spotify Premium. Музыка без рекламы и в оффлайне.",
        "image_url": "https://placehold.co/400x300/1db954/ffffff?text=Spotify+3M",
    },
    {
        "name": "Apple Music Gift Card $10",
        "category": "entertainment",
        "price": Decimal("10.00"),
        "description": "Подарочная карта Apple Music для оплаты подписки.",
        "image_url": "https://placehold.co/400x300/fc3c44/ffffff?text=Apple+Music",
    },
    {
        "name": "Binance Gift Card $100",
        "category": "crypto",
        "price": Decimal("100.00"),
        "description": "Подарочная карта Binance. Пополните аккаунт и начните торговлю криптовалютой.",
        "image_url": "https://placehold.co/400x300/f0b90b/000000?text=Binance+$100",
    },
    {
        "name": "Coinbase Gift Card $50",
        "category": "crypto",
        "price": Decimal("50.00"),
        "description": "Подарочная карта Coinbase для покупки Bitcoin, Ethereum и других криптовалют.",
        "image_url": "https://placehold.co/400x300/0052ff/ffffff?text=Coinbase+$50",
    },
    {
        "name": "Visa Prepaid Card $200",
        "category": "payment",
        "price": Decimal("200.00"),
        "description": "Предоплаченная карта Visa. Используйте везде, где принимают Visa.",
        "image_url": "https://placehold.co/400x300/1a1f71/ffffff?text=Visa+$200",
    },
    {
        "name": "Mastercard Prepaid $100",
        "category": "payment",
        "price": Decimal("100.00"),
        "description": "Предоплаченная карта Mastercard. Оплачивайте покупки онлайн и оффлайн.",
        "image_url": "https://placehold.co/400x300/eb001b/ffffff?text=MC+$100",
    },
    {
        "name": "Amazon Gift Card $50",
        "category": "payment",
        "price": Decimal("50.00"),
        "description": "Подарочная карта Amazon. Миллионы товаров на выбор.",
        "image_url": "https://placehold.co/400x300/ff9900/000000?text=Amazon+$50",
    },
    {
        "name": "Google Play Gift Card $25",
        "category": "entertainment",
        "price": Decimal("25.00"),
        "description": "Подарочная карта Google Play для покупки приложений, игр, фильмов и книг.",
        "image_url": None,
    },
]


async def seed_database():
    async with async_session() as session:
        # Проверяем, есть ли уже данные
        result = await session.execute(select(Product).limit(1))
        if result.scalar_one_or_none():
            print("Database already seeded, skipping.")
            return

        print("Seeding database...")

        # Создаём продукты
        products = []
        for data in PRODUCTS:
            product = Product(id=uuid.uuid4(), **data)
            session.add(product)
            products.append(product)

        await session.flush()

        now = datetime.now(timezone.utc)

        # Создаём гифт-карты
        gift_cards_data = [
            # Активные карты с разным балансом
            {
                "code": "BXTY-AAAA-1111-AAAA",
                "product": products[0],  # Steam $50
                "initial_balance": Decimal("50.00"),
                "balance": Decimal("50.00"),
                "status": "active",
                "expires_at": now + timedelta(days=365),
            },
            {
                "code": "BXTY-BBBB-2222-BBBB",
                "product": products[2],  # PS Store $25
                "initial_balance": Decimal("25.00"),
                "balance": Decimal("25.00"),
                "status": "active",
                "expires_at": now + timedelta(days=180),
            },
            {
                "code": "BXTY-CCCC-3333-CCCC",
                "product": products[9],  # Binance $100
                "initial_balance": Decimal("100.00"),
                "balance": Decimal("73.50"),
                "status": "active",
                "expires_at": now + timedelta(days=90),
            },
            {
                "code": "BXTY-DDDD-4444-DDDD",
                "product": products[11],  # Visa $200
                "initial_balance": Decimal("200.00"),
                "balance": Decimal("12.35"),
                "status": "active",
                "expires_at": now + timedelta(days=30),
            },
            # Просроченная карта
            {
                "code": "BXTY-EEEE-5555-EEEE",
                "product": products[6],  # Netflix $30
                "initial_balance": Decimal("30.00"),
                "balance": Decimal("15.00"),
                "status": "expired",
                "expires_at": now - timedelta(days=10),
            },
            # Заблокированная карта
            {
                "code": "BXTY-FFFF-6666-FFFF",
                "product": products[1],  # Steam $100
                "initial_balance": Decimal("100.00"),
                "balance": Decimal("100.00"),
                "status": "blocked",
                "expires_at": now + timedelta(days=365),
            },
            # Полностью использованная карта
            {
                "code": "BXTY-GGGG-7777-GGGG",
                "product": products[3],  # PS Store $50
                "initial_balance": Decimal("50.00"),
                "balance": Decimal("0.00"),
                "status": "redeemed",
                "expires_at": now + timedelta(days=200),
            },
            # Ещё одна активная карта (без срока действия)
            {
                "code": "BXTY-HHHH-8888-HHHH",
                "product": products[13],  # Amazon $50
                "initial_balance": Decimal("50.00"),
                "balance": Decimal("37.00"),
                "status": "active",
                "expires_at": None,
            },
        ]

        for data in gift_cards_data:
            product = data.pop("product")
            card = GiftCard(id=uuid.uuid4(), product_id=product.id, **data)
            session.add(card)

        await session.commit()
        print(f"Seeded {len(products)} products and {len(gift_cards_data)} gift cards.")


if __name__ == "__main__":
    asyncio.run(seed_database())
