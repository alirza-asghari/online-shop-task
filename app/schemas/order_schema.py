from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)

class OrderOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: str
    total_price: int

    model_config = ConfigDict(from_attributes=True)


class CheckoutRequest(BaseModel):
    # For demonstration, maybe the user provides a payment method, etc.
    payment_method: str
