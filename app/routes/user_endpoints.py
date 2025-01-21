from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserOut, UserLogin
from app.models.users import User
from app.utils.password_utils import hash_password
from app.controllers.user_controller import UserController
from database.database_connection import get_db_session
from app.config import config

class UserEndpoint(APIRouter):
    def __init__(self):
        super().__init__(prefix="/users", tags=["User Endpoints"])
        self.__setup_routes()

    def __setup_routes(self):
        self.add_api_route("/create/", self.create_user, methods=["POST"], response_model=UserOut)
        self.add_api_route("/get-user/", self.get_all_users, methods=["GET"], response_model=list[UserOut])
        self.add_api_route("/delete", self.delete_user, methods=["DELETE"], response_model=dict[str, str])
        self.add_api_route("/login", self.login, methods=["POST"], response_model=dict[str, str])

    def create_user(self, user_in: UserCreate, db: Session = Depends(get_db_session)) -> UserOut:
        """
        Creates a new user.

        Args:
            user_in (UserCreate): The new user's information.
            db (Session): The database session.

        Returns:
            UserOut: The newly created user.

        Raises:
            HTTPException: If the username is already registered or other errors occur.
        """
        return UserController.create_user(db, user=user_in)
        

    def get_all_users(self, db: Session = Depends(get_db_session)) -> list[UserOut]:
        """
        Retrieves all users. Only accessible by admin users.

        Args:
            db (Session): Database session.

        Returns:
            List[UserOut]: List of Pydantic models containing user information.

        Raises:
            HTTPException: If there's an error retrieving users.
        """
        return UserController.get_users(db)
        

    def delete_user(self, username: str, db: Session = Depends(get_db_session)) -> dict[str, str]:
        """
        Deletes a user from the database.

        Args:
            username (str): Username of the user to delete.
            db (Session): Database session.

        Returns:
            Dict[str, str]: Message indicating the result.

        Raises:
            HTTPException: If user does not exist or if there's an error during deletion.
        """
        return UserController.delete_user(db, username)
        
    def login(self, user_credentials: UserLogin, db: Session = Depends(get_db_session)) -> dict[str, str]:
        """
        Authenticates a user and returns a JWT token.

        Args:
            user_credentials (UserCreate): The user's login credentials.

        Returns:
            dict[str, str]: A dictionary containing the access token and token type.

        Raises:
            HTTPException: If authentication fails.
        """
        return UserController.login_user(db, user_credentials)