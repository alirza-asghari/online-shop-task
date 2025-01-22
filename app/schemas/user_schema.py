from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., examples=["user"])
    password: str = Field(..., min_length=8, examples=["password"])
    email: EmailStr

class UserLogin(BaseModel):
    username: str = Field(..., examples=["user"])
    password: str = Field(..., min_length=8, examples=["password"])

class UserOut(BaseModel):
    id: int
    username: str