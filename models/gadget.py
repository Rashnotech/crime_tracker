#!/usr/bin/env python3
"""a gadget model"""
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from .user import User
from .base import BaseModel


class Gadget(BaseModel, SQLModel, table=True):
    """
        Gadget class that implements the gadget model
    """
    phone_name: str = Field(max_length=50, required=True)
    browser: str = Field(max_length=50, required=True)
    os: str = Field(max_length=50, required=True)
    ip_address: str = Field(index=True, max_length=50, required=True)
    state: str = Field(max_length=50, required=True)
    user_id: str = Field(foreign_key='users.id', required=True, ondelete="CASCADE")

    def __init__(self, **kwargs):
        """Initialization"""
        super().__init__(**kwargs)