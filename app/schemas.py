from pydantic import BaseModel
from typing import List
from datetime import datetime


class SellerBase(BaseModel):
    id: int
    name: str


class ShopBase(BaseModel):
    id: int
    name: str


class BrandBase(BaseModel):
    id: int
    name: str


class ProductBase(BaseModel):
    id: int
    sku: str
    name: str


class SaleBase(BaseModel):
    id: int
    category_id: int
    price: float
    sales_volume: int
    revenue: float
    feedbacks_count: int
    created_at: datetime

    seller: SellerBase
    shop: ShopBase
    brand: BrandBase
    product: ProductBase


class CategoryResponse(BaseModel):
    category_id: int
    sales: List[SaleBase]


class SellerResponse(BaseModel):
    seller: SellerBase
    sales: List[SaleBase]


class ProductResponse(BaseModel):
    products: List[ProductBase]