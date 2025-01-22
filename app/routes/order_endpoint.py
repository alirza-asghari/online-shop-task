from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.order_schema import OrderCreate, CheckoutRequest, OrderOut
from app.controllers.order_controller import OrderController
from database.database_connection import get_db_session
from app.utils.dependency_utils import get_current_user

class CartEndpoint(APIRouter):
    def __init__(self):
        super().__init__(prefix="/cart", tags=["Cart Endpoints"])
        self.__setup_routes()

    def __setup_routes(self):
        # Route to add a product to cart
        self.add_api_route(
            "/add/", 
            self.add_to_cart, 
            methods=["POST"], 
            response_model=OrderOut, 
            dependencies=[Depends(get_current_user)]
        )
        # Route to remove a product from cart
        self.add_api_route(
            "/remove/{product_id}/", 
            self.remove_from_cart, 
            methods=["DELETE"], 
            response_model=dict[str, str], 
            dependencies=[Depends(get_current_user)]
        )
        # Route to view cart items
        self.add_api_route(
            "/", 
            self.view_cart, 
            methods=["GET"], 
            response_model=list[OrderOut], 
            dependencies=[Depends(get_current_user)]
        )
        # Route to checkout
        self.add_api_route(
            "/checkout/", 
            self.checkout, 
            methods=["POST"], 
            response_model=dict[str, str], 
            dependencies=[Depends(get_current_user)]
        )
        # Route to history of orders
        self.add_api_route(
        "/history/", 
        self.order_history, 
        methods=["GET"], 
        response_model=list[OrderOut], 
        dependencies=[Depends(get_current_user)]
        )

    def add_to_cart(
        self, 
        order_data: OrderCreate, 
        db: Session = Depends(get_db_session), 
        current_user = Depends(get_current_user)
    ) -> OrderOut:
        """
        Adds a product to the user's cart.
        """
        print(current_user.id)
        return OrderController.add_to_cart(db, current_user.id, order_data)

    def remove_from_cart(
        self, 
        product_id: int, 
        db: Session = Depends(get_db_session), 
        current_user = Depends(get_current_user)
    ) -> dict[str, str]:
        """
        Removes a product from the user's cart.
        """
        return OrderController.remove_from_cart(db, current_user.id, product_id)

    def view_cart(
        self, 
        db: Session = Depends(get_db_session), 
        current_user = Depends(get_current_user)
    ) -> list[OrderOut]:
        """
        Retrieves all items in the user's cart.
        """
        return OrderController.get_cart(db, current_user.id)

    def checkout(
        self, 
        checkout_data: CheckoutRequest, 
        db: Session = Depends(get_db_session), 
        current_user = Depends(get_current_user)
    ) -> dict[str, str]:
        """
        Processes checkout for all items in the cart.
        """
        return OrderController.checkout(db, current_user.id, checkout_data)

    def order_history(
        self,
        db: Session = Depends(get_db_session), 
        current_user = Depends(get_current_user)
    ) -> list[OrderOut]:
        """
        Retrieves the authenticated user's past orders.
        """
        return OrderController.get_order_history(db, current_user.id)