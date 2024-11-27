#!/usr/bin/env python3
"""a base model"""
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field
from . import storage


class BaseModel(BaseModel):
    """
        BaseModel class that implements
    """
    id = Field(default_factory=lambda: str(uuid4()), required=True)
    created_at = Field(default=datetime.now())
    updated_at = Field(default=datetime.now(), onupdate=datetime.now())

    def __init__(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.fromisoformat(value))
                elif key == '__class__':
                    del key
                else:
                    setattr(self, key, value)
        else:
            self.id: str = Field(default_factory=lambda: str(uuid4()), required=True)
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
    
    def save(self):
        """save a model to the session"""
        storage.new(self)
        storage.save()