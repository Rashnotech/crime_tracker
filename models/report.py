#!/usr/bin/env python3
"""a report model"""
from sqlmodel import Field, SQLModel, Relationship
from incident import Incident
from .base import BaseModel


class Report(BaseModel, SQLModel, table=True):
    """
        Report class that implements the report model
    """
    title: str = Field(max_length=50, required=True)
    incident_id: str = Field(foreign_key="incident.id", required=True)
    incident: Incident | None = Relationship(back_populates="reports")
    
    def __init__(self, **kwargs):
        """initialization"""
        super().__init__(**kwargs)