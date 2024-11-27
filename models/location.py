#!/usr/bin/env python3
"""a location model"""
from sqlmodel import Field, SQLModel
from pydantic import BaseModel


class Location(BaseModel, SQLModel, table=True):
    """
    Location Model
    """
    address: str = Field(max_length=50, required=True)
    city: str = Field(max_length=50, required=True)
    state: str = Field(max_length=50, required=True)
    zip: str = Field(max_length=5, required=True)