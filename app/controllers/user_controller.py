from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.users import User
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import create_access_token
from app.schemas.user_schema import UserCreate, UserOut, UserLogin
from app.tasks.email import send_verification_email
from app.config import config
from datetime import timedelta

class UserController:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserOut:
        """
        Creates a new user in the database.

        Args:
            db (Session): Database session.
            user (UserCreate): Pydantic model containing user creation data.

        Returns:
            UserOut: Pydantic model containing created user information.

        Raises:
            HTTPException: If username already exists or if there's an error during creation.
        """
        # Check if username already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists."
            )

        hashed_pw = hash_password(user.password)
        new_user = User(
            username = user.username,
            hashed_password = hashed_pw,
            email = user.email
        )

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}"
            )
        
        send_verification_email.delay(new_user.email)
        
        return UserOut(
            id=int(new_user.id),
            username=str(new_user.username)
        )
    
    @staticmethod
    def delete_user(db: Session, username: str) -> dict[str, str]:
        """
        Deletes a user from the database.

        Args:
            db (Session): Database session.
            username (str): Username of the user to delete.

        Returns:
            dict[str, str]: Message indicating the result.

        Raises:
            HTTPException: If user does not exist or if there's an error during deletion.
        """
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        try:
            db.delete(user)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting user: {str(e)}"
            )

        return {"detail": f"User '{username}' has been deleted successfully."}
    
    @staticmethod
    def get_users(db: Session) -> list[UserOut]:
        """
        Retrieves all users from the database.

        Args:
            db (Session): Database session.

        Returns:
            list[UserOut]: list of Pydantic models containing user information.
        """
        users = db.query(User).all()
        user_out_list = []
        for user in users:
            user_out = UserOut(
                id=int(user.id),
                username=str(user.username),
            )
            user_out_list.append(user_out)
        return user_out_list
    
    @staticmethod
    def login_user(db: Session, user_credentials: UserLogin) -> dict[str, str]:
        """
        Retrieves all users from the database.

        Args:
            db (Session): Database session.

        Returns:
            dict[str, str]: A dictionary containing the access token and token type.
        """
        try:
            user = db.query(User).filter(User.username == user_credentials.username).first()
            if not user or not verify_password(user_credentials.password, str(user.hashed_password)):
                raise HTTPException(status_code=401, detail="Incorrect username or password")
            
            access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username, "email": user.email},
                expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))