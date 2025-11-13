import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, AsyncSessionLocal, create_tables
from app.models import Seller, Shop, Brand, Product, Sale
from sqlalchemy import select


async def create_test_data():
    # Сначала создаем таблицы если их нет
    await create_tables()
    print("✅ Database tables created/verified")

    async with AsyncSessionLocal() as session:
        print("🔄 Creating test data...")

        try:
            # Проверяем, есть ли уже данные
            result = await session.execute(select(Seller))
            existing_sellers = result.scalars().all()

            if existing_sellers:
                print("✅ Data already exists in database!")
                print(f"   Found {len(existing_sellers)} sellers")
                return

            # Создаем тестовые данные
            seller1 = Seller(name="Иван Иванов")
            seller2 = Seller(name="Петр Петров")

            shop1 = Shop(name="Магазин Одежды")
            shop2 = Shop(name="СпортМастер")

            brand1 = Brand(name="Nike")
            brand2 = Brand(name="Adidas")

            product1 = Product(sku="NK001", name="Кроссовки Nike Air Max")
            product2 = Product(sku="AD001", name="Кроссовки Adidas Ultraboost")

            # Добавляем все в сессию
            all_objects = [seller1, seller2, shop1, shop2, brand1, brand2, product1, product2]
            session.add_all(all_objects)
            await session.commit()

            # Обновляем объекты чтобы получить их ID
            for obj in all_objects:
                await session.refresh(obj)

            # Создаем продажи
            sales_data = [
                Sale(category_id=123, seller_id=seller1.id, shop_id=shop1.id,
                     brand_id=brand1.id, product_id=product1.id,
                     price=4999.0, sales_volume=150, revenue=749850.0, feedbacks_count=45),

                Sale(category_id=123, seller_id=seller2.id, shop_id=shop2.id,
                     brand_id=brand2.id, product_id=product2.id,
                     price=3999.0, sales_volume=200, revenue=799800.0, feedbacks_count=38),
            ]

            session.add_all(sales_data)
            await session.commit()

            print("✅ Test data created successfully!")
            print(f"   Created: 2 sellers, 2 shops, 2 brands, 2 products, 2 sales")

        except Exception as e:
            print(f"❌ Error: {e}")
            await session.rollback()


if __name__ == "__main__":
    asyncio.run(create_test_data())