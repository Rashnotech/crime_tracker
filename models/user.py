#!/usr/bin/env python3
"""a base model"""
from typing import Tuple
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, Field, EmailStr
from .base import BaseModel
from hashlib import md5

class User(BaseModel, SQLModel, table=True):
    """
        BaseModel class that implements
    """
    username: str = Field(index=True, max_length=50, required=True)
    firstname: str = Field(max_length=50, required=True)
    lastname: str = Field(max_length=50, required=True)
    email: EmailStr = Field(max_length=50, required=True)
    telephone: str = Field(max_length=16, required=True)
    password: str = Field(max_length=50, required=True)
    validated: bool = Field(default=False)
    account_type: tuple[str, str] = Field(max_length=50, required=True)

    def __init__(self, **kwargs):
        """initialization"""
        super().__init__(**kwargs)
        self.password = md5(self.password.encode()).hexdigest()

    def is_validated(self):
        """check if user is validated"""
        return self.validated
    
    def set_password(self, new_password: str):
        """set password"""
        self.password = new_password