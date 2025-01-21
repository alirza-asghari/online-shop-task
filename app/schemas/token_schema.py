from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    sub: Optional[str] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str