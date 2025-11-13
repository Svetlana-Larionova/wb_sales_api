from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import crud, schemas, database
from .services import WoysaDataLoader

router = APIRouter()


@router.get("/category/{category_id}", response_model=schemas.CategoryResponse)
async def get_category_sales(category_id: int, db: AsyncSession = Depends(database.get_db)):
    crud_instance = crud.CRUD(db)
    sales = await crud_instance.get_sales_by_category(category_id)
    return schemas.CategoryResponse(category_id=category_id, sales=sales)


@router.get("/sellers/", response_model=List[schemas.SellerBase])
async def get_all_sellers(db: AsyncSession = Depends(database.get_db)):
    crud_instance = crud.CRUD(db)
    sellers = await crud_instance.get_all_sellers()
    return sellers


@router.get("/sellers/{seller_id}", response_model=schemas.SellerResponse)
async def get_seller_sales(seller_id: int, db: AsyncSession = Depends(database.get_db)):
    crud_instance = crud.CRUD(db)
    sales = await crud_instance.get_sales_by_seller(seller_id)
    if not sales:
        raise HTTPException(status_code=404, detail="Seller not found")
    return schemas.SellerResponse(seller=sales[0].seller, sales=sales)


@router.get("/products/", response_model=schemas.ProductResponse)
async def get_all_products(db: AsyncSession = Depends(database.get_db)):
    crud_instance = crud.CRUD(db)
    products = await crud_instance.get_all_products()
    return schemas.ProductResponse(products=products)


@router.post("/update/{category_id}")
async def update_data(category_id: int, db: AsyncSession = Depends(database.get_db)):
    loader = WoysaDataLoader()
    data = await loader.fetch_category_data(category_id)

    if not data:
        return {"message": "No data received from API"}

    crud_instance = crud.CRUD(db)
    count = 0

    for item in data:
        try:
            sale_data = {
                'category_id': category_id,
                'seller_name': item.get('seller_name', 'Unknown'),
                'shop_name': item.get('shop_name', 'Unknown'),
                'brand_name': item.get('brand_name', 'Unknown'),
                'sku': item.get('sku', f"unknown_{count}"),
                'product_name': item.get('product_name', 'Unknown'),
                'price': float(item.get('price', 0)),
                'sales_volume': int(item.get('sales_volume', 0)),
                'revenue': float(item.get('revenue', 0)),
                'feedbacks_count': int(item.get('feedbacks_count', 0))
            }
            await crud_instance.create_sale(sale_data)
            count += 1
        except Exception as e:
            print(f"Error processing item: {e}")
            continue

    return {"message": f"Successfully added {count} sales records for category {category_id}"}