#!/usr/bin/env python3
"""a report model"""
from typing import Optional
from sqlmodel import Field
from datetime import datetime
from entity.crime_entity import CrimeCategory
from base import BaseModel


class CrimeReportBase(BaseModel):
    reporter_id: int = Field(foreign_key="user.id")
    category: CrimeCategory
    description: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    incident_date: datetime
    report_date: datetime = Field(default_factory=datetime.utcnow)
    is_verified: bool = False
    is_resolved: bool = False