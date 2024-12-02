#!/usr/bin/env python3
"""a user model"""
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from crime import CrimeReport
from entity.device_entity import DeviceType
from datetime import datetime, timezone
from base import BaseModel


class UserBase(BaseModel):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_verified: bool = False
    is_active: bool = False
    disable: Optional[bool] = None


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    devices: List["UserDevice"] = Relationship(back_populates="user")
    crime_reports: List["CrimeReport"] = Relationship(back_populates="reporter")

class UserInDB(UserBase):
    hashed_password: str

class UserDeviceBase(BaseModel):
    user_id: int = Field(foreign_key="user.id")
    device_type: DeviceType
    device_id: str
    ip_address: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None
    last_used: datetime = Field(default_factory=datetime.now(timezone.utc))


class UserDevice(UserDeviceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    user: User = Relationship(back_populates="devices")
