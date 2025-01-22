from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    name: str
    price: int

class ProductUpdate(ProductCreate):
    pass

class ProductsDetail(BaseModel):
    id: int
    name: str
    price: int

    model_config = ConfigDict(from_attributes=True)