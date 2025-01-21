from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: int

class ProductUpdate(ProductCreate):
    pass

class ProductsDetail(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True