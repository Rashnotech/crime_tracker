#!/usr/bin/python3
"""a middleware authentication """
from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select
from models.user import User
from os import getenv


# Security configuration
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str


class AuthManager:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against its hashed version
        
        Args:
            plain_password (str): Plain text password
            hashed_password (str): Hashed password to compare against
        
        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a plain text password
        
        Args:
            password (str): Plain text password
        
        Returns:
            str: Hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(
        data: dict, 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token
        
        Args:
            data (dict): Payload data for the token
            expires_delta (Optional[timedelta]): Token expiration time
        
        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()
        
        # Set expiration time
        if expires_delta:
            expire = datetime.now(timezone.utcnow) + expires_delta
        else:
            expire = datetime.now(timezone.utcnow) + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        
        # Encode the token
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


class AuthRepository:
    """
    Authentication repository for database operations
    """
    @staticmethod
    def get_user_by_username(session: Session, username: str):
        """
        Retrieve a user by username from the database
        
        Args:
            session (Session): Database session
            username (str): Username to search for
        
        Returns:
            Optional[User]: User object if found
        """
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

    @staticmethod
    def authenticate_user(
        session: Session, 
        username: str, 
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user
        
        Args:
            session (Session): Database session
            username (str): Username
            password (str): Plain text password
        
        Returns:
            Optional[User]: Authenticated user or None
        """
        user = AuthRepository.get_user_by_username(session, username)
        
        if not user:
            return None
        
        if not AuthManager.verify_password(password, user.hashed_password):
            return None
        
        return user

class AuthMiddleware:
    """
    Authentication middleware for route protection
    """
    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session
    ) -> User:
        """
        Get the current authenticated user from JWT token
        
        Args:
            token (str): JWT access token
            session (Session): Database session
        
        Returns:
            User: Authenticated user
        
        Raises:
            HTTPException: If token is invalid or user not found
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
        try:
            # Decode the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            
            if username is None:
                raise credentials_exception
            
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        
        # Fetch user from database
        user = AuthRepository.get_user_by_username(
            session, 
            username=token_data.username
        )
        
        if user is None:
            raise credentials_exception
        
        return user

    @staticmethod
    async def get_current_active_user(
        current_user: Annotated[User, Depends(AuthMiddleware.get_current_user)]
    ) -> User:
        """
        Get the current active user
        
        Args:
            current_user (User): Authenticated user
        
        Returns:
            User: Active user
        
        Raises:
            HTTPException: If user is disabled
        """
        if getattr(current_user, 'disabled', False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Inactive user"
            )
        return current_user

# Example protected route
def setup_protected_routes(app: FastAPI):
    """
    Setup routes that require authentication
    
    Args:
        app (FastAPI): FastAPI application instance
    """
    @app.get("/users/me/", response_model=User)
    async def read_users_me(
        current_user: Annotated[User, Depends(AuthMiddleware.get_current_active_user)]
    ):
        """
        Get the current user's information
        Requires a valid JWT token
        """
        return current_user
