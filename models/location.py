#!/usr/bin/env python3
"""a location model"""
from sqlmodel import Field, SQLModel, Relationship
from .base import Base
from .incident import Incident


class Location(Base, SQLModel, table=True):
    """
    Location Model
    """
    address: str = Field(max_length=50, required=True)
    city: str = Field(max_length=50, required=True)
    state: str = Field(max_length=50, required=True)
    zip: str = Field(max_length=5, required=True)
    incidents_id: str = Field(foreign_key="incidents.id", required=True)
    incidents: Incident | None = Relationship(back_populates="locations")

    def __init__(self, **kwargs):
        """Initialization"""
        super().__init__(**kwargs)