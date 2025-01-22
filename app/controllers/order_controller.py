from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.orders import Order
from app.models.products import Product
from app.schemas.order_schema import OrderCreate, OrderOut, CheckoutRequest
from app.models.users import User

class OrderController:

    @staticmethod
    def add_to_cart(db: Session, user_id: int, order_create: OrderCreate) -> OrderOut:
        """
        Add a product to the user's cart. If the product is already in cart, increase quantity.
        """
        # 1) Check if product exists
        product = db.query(Product).filter(Product.id == order_create.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )

        # 2) Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        # 3) Check if there's already an "in_cart" order for this product & user
        existing_order = db.query(Order).filter(
            Order.user_id == user_id,
            Order.product_id == order_create.product_id,
            Order.status == "in_cart"
        ).first()

        try:
            if existing_order:
                new_quantity = int(existing_order.quantity) + order_create.quantity
                setattr(existing_order, 'quantity', new_quantity)
                new_price = existing_order.total_price + order_create.quantity * product.price
                setattr(existing_order, 'total_price', new_price)
                db.commit()
                db.refresh(existing_order)
                return OrderOut.model_validate(existing_order)
            else:
                # Create new order item with status in_cart
                new_order = Order(
                    user_id=user_id,
                    product_id=order_create.product_id,
                    quantity=order_create.quantity,
                    status="in_cart",
                    total_price=product.price * order_create.quantity 
                )
                db.add(new_order)
                db.commit()
                db.refresh(new_order)
                return OrderOut.model_validate(new_order)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    @staticmethod
    def remove_from_cart(db: Session, user_id: int, product_id: int) -> dict[str, str]:
        """
        Remove a product from the user's cart (if it exists and is in_cart).
        """
        order_item = db.query(Order).filter(
            Order.user_id == user_id,
            Order.product_id == product_id,
            Order.status == "in_cart"
        ).first()

        if not order_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found in cart."
            )
        
        try:
            db.delete(order_item)
            db.commit()
            return {"detail": "Product removed from cart."}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    @staticmethod
    def get_cart(db: Session, user_id: int) -> list[OrderOut]:
        """
        Retrieve all 'in_cart' items for a specific user.
        """
        orders = db.query(Order).filter(
            Order.user_id == user_id,
            Order.status == "in_cart"
        ).all()

        return [OrderOut.model_validate(o) for o in orders]

    @staticmethod
    def checkout(db: Session, user_id: int, checkout_data: CheckoutRequest) -> dict[str, str]:
        """
        Mark all 'in_cart' items as 'paid'. In real scenario, integrate payment gateway.
        """
        in_cart_items = db.query(Order).filter(
            Order.user_id == user_id,
            Order.status == "in_cart"
        ).all()

        if not in_cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No items in cart to check out."
            )

        try:
            total_cost = 0
            for item in in_cart_items:
                # If you want to store total_price, do so here:
                # e.g., item.total_price = item.quantity * item.product.price
                item.total_price = item.quantity * item.product.price
                total_cost += item.total_price
                item.status = "paid"
            
            db.commit()
            # Here you would call your payment service with `total_cost` and `checkout_data.payment_method`
            return {"detail": f"Payment successful. Total cost: {total_cost}"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
