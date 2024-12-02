#"""!/usr/bin/python3
"""a module for the base model"""
from typing import Optional
from uuid import uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy import func

class BaseModel(SQLModel):
    """
    Base model that provides common fields and functionality
    for all database models
    """
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        sa_column=Column('id', nullable=False, unique=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=func.now(), 
            onupdate=func.now()
        )
    )

    def __init__(self, **kwargs):
        """
        Custom initialization to handle different input formats
        """
        for date_field in ['created_at', 'updated_at']:
            if date_field in kwargs:
                value = kwargs[date_field]
                if isinstance(value, str):
                    kwargs[date_field] = datetime.fromisoformat(value)
        
        kwargs.pop('__class__', None)
        
        super().__init__(**kwargs)

    def __str__(self):
        """
        String representation of the model
        """
        return f"{self.__class__.__name__}({self.dict()})"

    def dict(self, *args, **kwargs):
        """
        Override dict method to include additional fields
        """
        exclude = kwargs.get('exclude', set())
        exclude.update({'id', 'created_at', 'updated_at'})
        kwargs['exclude'] = exclude
        
        return super().dict(*args, **kwargs)