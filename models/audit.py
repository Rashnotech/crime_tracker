#!/usr/bin/env python3
"""a audit log model"""
from typing import List, Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from base import BaseModel


class AuditLogBase(BaseModel):
    user_id: Optional[int] = Field(foreign_key="user.id", default=None)
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = None
    details: Optional[str] = None


class AuditLog(AuditLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
