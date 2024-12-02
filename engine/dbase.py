#!/usr/bin/env python3
"""A comprehensive database session management engine for crime tracker"""

from typing import Type, TypeVar, Optional, List, Generic
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import contextmanager
import logging

T = TypeVar('T', bound=SQLModel)

class DBSessionManager:
    """
    Advanced database session management class
    Provides comprehensive CRUD operations and session handling
    
    Attributes:
        __engine: SQLAlchemy engine for database connections
        __session: Current database session
    """

    def __init__(self, 
                 dbname: str = 'crime_tracker.db', 
                 echo: bool = False):
        """
        Initialize database engine and logging
        
        Args:
            dbname (str): Path to the SQLite database file
            echo (bool): Enable SQLAlchemy logging
        """
        try:
            self.__engine = create_engine(
                f'sqlite:///{dbname}', 
                connect_args={"check_same_thread": False},
                echo=echo
            )
            self.__session = None
            
            # Configure logging
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.INFO)
        except Exception as e:
            self.logger.error(f"Database initialization error: {e}")
            raise

    @contextmanager
    def session_scope(self):
        """
        Provide a transactional scope around a series of operations
        Automatically handles session commit and rollback
        """
        self.__session = Session(self.__engine, expire_on_commit=False)
        try:
            yield self.__session
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            self.logger.error(f"Session error: {e}")
            raise
        finally:
            self.__session.close()

    def create_tables(self):
        """
        Create all defined database tables
        """
        try:
            SQLModel.metadata.create_all(self.__engine)
            self.logger.info("Database tables created successfully")
        except Exception as e:
            self.logger.error(f"Error creating tables: {e}")
            raise

    def add(self, model: T) -> T:
        """
        Add a new model instance to the database
        
        Args:
            model (SQLModel): Model instance to add
        
        Returns:
            T: The added model with potential updated attributes
        """
        try:
            with self.session_scope() as session:
                session.add(model)
                session.flush()
                return model
        except Exception as e:
            self.logger.error(f"Error adding model: {e}")
            raise

    def get_by_id(self, model_class: Type[T], model_id: int) -> Optional[T]:
        """
        Retrieve a model instance by its ID
        
        Args:
            model_class (Type[T]): The SQLModel class
            model_id (int): The ID of the model to retrieve
        
        Returns:
            Optional[T]: The retrieved model or None
        """
        try:
            with self.session_scope() as session:
                return session.get(model_class, model_id)
        except Exception as e:
            self.logger.error(f"Error retrieving model: {e}")
            raise

    def query(self, model_class: Type[T], 
              filters: Optional[dict] = None, 
              limit: Optional[int] = None) -> List[T]:
        """
        Query models with optional filtering and limiting
        
        Args:
            model_class (Type[T]): The SQLModel class to query
            filters (Optional[dict]): Dictionary of filter conditions
            limit (Optional[int]): Maximum number of results
        
        Returns:
            List[T]: List of retrieved models
        """
        try:
            with self.session_scope() as session:
                statement = select(model_class)
                
                if filters:
                    for key, value in filters.items():
                        statement = statement.where(
                            getattr(model_class, key) == value
                        )
                
                if limit:
                    statement = statement.limit(limit)
                
                results = session.exec(statement).all()
                return results
        except Exception as e:
            self.logger.error(f"Error querying models: {e}")
            raise

    def update(self, model: T) -> T:
        """
        Update an existing model instance
        
        Args:
            model (T): Model instance to update
        
        Returns:
            T: The updated model
        """
        try:
            with self.session_scope() as session:
                db_model = session.get(type(model), model.id)
                if db_model:
                    for key, value in model.dict(exclude_unset=True).items():
                        setattr(db_model, key, value)
                    session.add(db_model)
                    return db_model
                raise ValueError("Model not found")
        except Exception as e:
            self.logger.error(f"Error updating model: {e}")
            raise

    def delete(self, model: T):
        """
        Delete a model instance
        
        Args:
            model (T): Model instance to delete
        """
        try:
            with self.session_scope() as session:
                session.delete(model)
        except Exception as e:
            self.logger.error(f"Error deleting model: {e}")
            raise

    def close(self):
        """
        Close the database connection
        """
        if self.__session:
            self.__session.close()