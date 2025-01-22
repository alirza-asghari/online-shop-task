from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.products import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductsDetail
from typing import Optional

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
        Retrieves all products from the database.

        Args:
            db (Session): Database session.

        Returns:
            list[ProductOut]: A list of all products.

        Raises:
            HTTPException: If there's an error retrieving products.
        """
        try:
            products = db.query(Product).limit(limit)
            if from_price and to_price:
                products = products.where(
                    (Product.price >= from_price) &
                    (Product.price <= to_price)) 
            product_list = []
            for product in products:
                product_out = ProductsDetail(
                    id=int(product.id),
                    name=str(product.name),
                    price=int(product.price)
                )
                product_list.append(product_out)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving products: {str(e)}"
            )

        return product_list
