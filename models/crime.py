#!/usr/bin/python3
"""a module for crime models"""
from typing import List, Optional
from sqlmodel import Field, Relationship
from datetime import datetime
from user import User
from report import CrimeReportBase
from base import BaseModel

class CrimeReport(CrimeReportBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    reporter: User = Relationship(back_populates="crime_reports")
    media_files: List["CrimeMediaFile"] = Relationship(back_populates="crime_report")

class CrimeMediaFileBase(BaseModel):
    crime_report_id: int = Field(foreign_key="crimereport.id")
    file_path: str
    file_type: str  # 'image' or 'video'
    upload_date: datetime = Field(default_factory=datetime.utcnow)

class CrimeMediaFile(CrimeMediaFileBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    crime_report: CrimeReport = Relationship(back_populates="media_files")
