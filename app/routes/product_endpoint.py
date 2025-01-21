from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductsDetail
from app.controllers.product_controller import ProductController
from database.database_connection import get_db_session
from app.utils.dependency_utils import get_current_user
from app.config import config

class ProductEndpoint(APIRouter):
    def __init__(self):
        super().__init__(prefix="/products", tags=["Product Endpoints"])
        self.__setup_routes()

    def __setup_routes(self):
        self.add_api_route("/create/", self.create_product, methods=["POST"], response_model=dict[str, str], dependencies=[Depends(get_current_user)])
        self.add_api_route("/update/{product_id}/", self.update_product, methods=["PUT"], response_model=dict[str, str], dependencies=[Depends(get_current_user)])
        self.add_api_route("/delete/{product_id}/", self.delete_product, methods=["DELETE"], response_model=dict[str, str], dependencies=[Depends(get_current_user)])
        self.add_api_route("/all/", self.get_all_products, methods=["GET"], response_model=list[ProductsDetail], dependencies=[Depends(get_current_user)])

    def create_product(self, product_in: ProductCreate, db: Session = Depends(get_db_session)) -> dict[str, str]:
        """
        Creates a new product.

        Args:
            product_in (ProductCreate): The new product's information.
            db (Session): The database session.

        Returns:
            ProductOut: The newly created product.
        """
        return ProductController.create_product(db, product_in)

    def update_product(self, product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db_session)) -> dict[str, str]:
        """
        Updates an existing product.

        Args:
            product_id (int): ID of the product to update.
            product_update (ProductUpdate): The updated product information.
            db (Session): The database session.

        Returns:
            ProductOut: The updated product.
        """
        return ProductController.update_product(db, product_id, product_update)

    def delete_product(self, product_id: int, db: Session = Depends(get_db_session)) -> dict[str, str]:
        """
        Deletes a product.

        Args:
            product_id (int): ID of the product to delete.
            db (Session): The database session.

        Returns:
            dict[str, str]: Message indicating the result.

        """
        return ProductController.delete_product(db, product_id)


    def get_all_products(self, db: Session = Depends(get_db_session)) -> list[ProductsDetail]:
        """
        Retrieves all products.

        Args:
            db (Session): Database session.

        Returns:
            list[ProductOut]: List of products.
        """

        return ProductController.get_products(db)
