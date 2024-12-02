#!/usr/bin/env python3
"""a module for auth routes"""
from app.middleware.auth import AuthManager, AuthRepository, Token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from engine.dbase import DBSessionManager, Session

router = APIRouter()
db_manager = DBSessionManager()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(db_manager.session_scope)
):
    """
    OAuth2 compatible token login endpoint
    """
    user = AuthRepository.authenticate_user(
        session, 
        form_data.username, 
        form_data.password
    )

    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthManager.create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }