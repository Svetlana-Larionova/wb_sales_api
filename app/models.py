from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Seller(Base):
    __tablename__ = "sellers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    sales = relationship("Sale", back_populates="seller")


class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    sales = relationship("Sale", back_populates="shop")


class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    sales = relationship("Sale", back_populates="brand")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    name = Column(String)
    sales = relationship("Sale", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    shop_id = Column(Integer, ForeignKey("shops.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float)
    sales_volume = Column(Integer)
    revenue = Column(Float)
    feedbacks_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    seller = relationship("Seller", back_populates="sales")
    shop = relationship("Shop", back_populates="sales")
    brand = relationship("Brand", back_populates="sales")
    product = relationship("Product", back_populates="sales")