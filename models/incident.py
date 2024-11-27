#!/usr/bin/env python3
"""a crime tracker model"""
from uuid import uuid4
from datetime import datetime
from location import Location
from sqlmodel import Field, SQLModel, Relationship
from .base import BaseModel
from category import Category
from .report import Report

class Incident(BaseModel, SQLModel, table=True):
    """
    Incident Model
    """
    title: str = Field(max_length=50, required=True)
    description: str = Field(max_length=50, required=True)
    pictures: list[str] = Field(default=[])
    videos: list[str] = Field(default=[])
    location: Location = Field(max_length=50, required=True)
    category: Category = Field(max_length=50, required=True)
    report: Report | None = Relationship(back_populates="incident")

    def __init__(self, kwargs):
        """initialize the incident model"""
        super().__init__(kwargs)