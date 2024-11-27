#!/usr/bin/env python3
"""a crime tracker engine"""
from sqlmodel import Field, Session, SQLModel, create_engine
from fastapi import Depends, FastAPI, HTTPException, Query
from typing import Annotated


class DBSession:
    """
        DBStorage class that implements the CRUD operations
        Attrs:
            __engine: a private attribute
            __session: a private attribute
    """
    __engine = None
    __session = None

    def __init__(self, dbname: str):
        self.__engine = create_engine(f'sqlite:///{dbname}', connect_args={"check_same_thread": False})

    def new(self, model: SQLModel):
        """
            creates a new session
        """
        self.__session = Session(bind=self.__engine, expire_on_commit=False)

    def commit(self):
        self.__session.commit()
    
    def add(self, model: SQLModel):
        """add a model to the session"""
        self.__session.add(model)

    def all(self, model: SQLModel):
        """get a model from the session"""
        return self.__session.get(model)
    
    def get(self, model: SQLModel, id: int):
        """get a model from the session"""
        return self.__session.get(model, id)
    
    def query(self, model: SQLModel):
        """query the session"""
        return self.__session.query(model)
    
    def save(self, model: SQLModel):
        """save a model to the session"""
        self.add(model)
        self.__session.commit()
        self.__session.refresh(model)

    def reload(self):
        """
            reloads the session
        """
        SQLModel.metadata.create_all(self.__engine)
        session = Session(bind=self.__engine, expire_on_commit=False)
        self.__session = session

    def delete(self, model: SQLModel):
        """
            deletes a model from the session
        """
        if model:
            self.__session.delete(model)

    def close(self):
        """close this session"""
        self.__session.close()