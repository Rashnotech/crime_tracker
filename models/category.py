#!/usr/bin/env python3
"""a crime tracker category model"""
from .base import Base
from sqlmodel import Field, SQLModel


class Category(Base, SQLModel):
    """
        Category class that implements the category model
    """
    name: str = Field(max_length=50, required=True)
    description: str = Field(max_length=50, required=True)

    def __init__(self, **kwargs):
        """initialize the category model"""
        super().__init__(**kwargs)
