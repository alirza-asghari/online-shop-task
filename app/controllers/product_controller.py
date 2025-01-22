from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.products import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductsDetail
from app.utils.redis_utils import get_cache, set_cache
from typing import Optional
import json

class ProductController:
    """
    Controller class for managing products based on product model.
    """
    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> dict[str, str]:
        """
        Creates a new product in the database.

        Args:
            db (Session): Database session.
            product (ProductCreate): Pydantic model containing product creation data.

        Returns:
            str: A message indicating the product has been created.

        Raises:
            HTTPException: If there's an error during creation.
        """
        new_product = Product(
            name=product.name,
            price=product.price
        )

        try:
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating product: {str(e)}"
            )

        return {'detail' : f'Product {new_product.name} created'}

    @staticmethod
    def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> dict[str, str]:
        """
        Updates an existing product in the database.

        Args:
            db (Session): Database session.
            product_id (int): ID of the product to update.
            product_update (ProductUpdate): Pydantic model containing product update data.

        Returns:
            ProductOut: The updated product object.

        Raises:
            HTTPException: If the product is not found or there's an error during update.
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )

        # Update the product fields
        setattr(product, 'name', product_update.name)
        setattr(product, 'price', product_update.price)

        try:
            db.commit()
            db.refresh(product)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating product: {str(e)}"
            )

        return {"detail": f"Product {product_id} updated"}

    @staticmethod
    def delete_product(db: Session, product_id: int) -> dict[str, str]:
        """
        Deletes a product from the database.

        Args:
            db (Session): Database session.
            product_id (int): ID of the product to delete.

        Returns:
            dict[str, str]: A message indicating the deletion status.

        Raises:
            HTTPException: If the product is not found or there's an error during deletion.
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )

        try:
            db.delete(product)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting product: {str(e)}"
            )

        return {"detail": f"Product {product_id} deleted"}

    @staticmethod
    def get_products(db: Session,
        limit: Optional[int] = 10,
        from_price: Optional[int] = None,
        to_price: Optional[int] = None
    )-> list[ProductsDetail]:
        """
        Retrieves all products from the database or redis(cache).

        Args:
            db (Session): Database session.

        Returns:
            list[ProductOut]: A list of all products.

        Raises:
            HTTPException: If there's an error retrieving products.
        """
        cache_key = f"products:{limit}:{from_price}:{to_price}"

        # 2) Attempt to get data from Redis
        cached_data = get_cache(cache_key)
        if cached_data:
            # If we have something in Redis, parse the JSON-serialized list
            try:
                return [ProductsDetail(**prod) for prod in json.loads(cached_data)]
            except Exception as e:
                # If JSON parse fails for some reason, we can log or ignore and fall back
                pass

        # 3) If not cached, query the DB
        try:
            query = db.query(Product).limit(limit)

            if from_price is not None and to_price is not None:
                query = query.filter(Product.price >= from_price, Product.price <= to_price)

            products = query.all()

            # 4) Convert to the schema
            product_list = [
                ProductsDetail(id=int(p.id), name=str(p.name), price=int(p.price))
                for p in products
            ]

            # 5) Store in cache (e.g., for 2 minutes = 120 seconds)
            set_cache(cache_key, json.dumps([prod.model_dump() for prod in product_list]), expire=120)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving products: {str(e)}"
            )

        return product_list
