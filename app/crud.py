from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from . import models
from typing import List


class CRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create(self, model, **kwargs):
        name_field = list(kwargs.keys())[0]
        name_value = list(kwargs.values())[0]

        result = await self.db.execute(
            select(model).where(getattr(model, name_field) == name_value)
        )
        instance = result.scalar_one_or_none()

        if not instance:
            instance = model(**kwargs)
            self.db.add(instance)
            await self.db.commit()
            await self.db.refresh(instance)

        return instance

    async def create_sale(self, sale_data: dict):
        seller = await self.get_or_create(models.Seller, name=sale_data['seller_name'])
        shop = await self.get_or_create(models.Shop, name=sale_data['shop_name'])
        brand = await self.get_or_create(models.Brand, name=sale_data['brand_name'])
        product = await self.get_or_create(models.Product, sku=sale_data['sku'], name=sale_data['product_name'])

        sale = models.Sale(
            category_id=sale_data['category_id'],
            seller_id=seller.id,
            shop_id=shop.id,
            brand_id=brand.id,
            product_id=product.id,
            price=sale_data['price'],
            sales_volume=sale_data['sales_volume'],
            revenue=sale_data['revenue'],
            feedbacks_count=sale_data['feedbacks_count']
        )

        self.db.add(sale)
        await self.db.commit()
        await self.db.refresh(sale)
        return sale

    async def get_sales_by_category(self, category_id: int) -> List[models.Sale]:
        result = await self.db.execute(
            select(models.Sale)
            .where(models.Sale.category_id == category_id)
            .options(
                selectinload(models.Sale.seller),
                selectinload(models.Sale.shop),
                selectinload(models.Sale.brand),
                selectinload(models.Sale.product)
            )
        )
        return result.scalars().all()

    async def get_all_sellers(self) -> List[models.Seller]:
        result = await self.db.execute(select(models.Seller))
        return result.scalars().all()

    async def get_sales_by_seller(self, seller_id: int) -> List[models.Sale]:
        result = await self.db.execute(
            select(models.Sale)
            .where(models.Sale.seller_id == seller_id)
            .options(
                selectinload(models.Sale.seller),
                selectinload(models.Sale.shop),
                selectinload(models.Sale.brand),
                selectinload(models.Sale.product)
            )
        )
        return result.scalars().all()

    async def get_all_products(self) -> List[models.Product]:
        result = await self.db.execute(select(models.Product))
        return result.scalars().all()