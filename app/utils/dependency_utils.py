from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from database.database_connection import get_db_session
from app.models.users import User
from app.utils.jwt_utils import decode_access_token
from app.schemas.token_schema import TokenData
from app.config import config
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scheme_name="BearerAuth")
logger = logging.getLogger(__name__)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)) -> User:
    """
    Retrieves the current user based on the JWT token.

    Args:
        token (str): The JWT token extracted from the Authorization header.
        db (Session): The database session.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload: Optional[TokenData] = decode_access_token(token)
    if payload is None:
        logger.warning("Token could not be decoded.")
        raise credentials_exception
    
    username: Optional[str] = payload.sub
    if username is None:
        logger.warning("Username not found in token payload.")
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        logger.warning(f"User '{username}' not found in database.")
        raise credentials_exception
    
    logger.info(f"Authenticated user: {username}")
    return user