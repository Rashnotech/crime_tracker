#!/usr/bin/env python3
"""a module for authentication middleware"""
from datetime import timedelta, timezone, datetime
from fastapi import FastAPI, Request
from fastapi import Depends, FastAPI, HTTPException, status
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import current_user
from os import environ
from pydantic import BaseModel


# CONSTANTS
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

@current_user.post()
async def access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """a route to get an access token"""
    pass


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """a function to create an access token"""
    pass