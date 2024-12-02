#!/usr/bin/env python3
"""a crime tracker server"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users
from engine.dbase import DBSessionManager


app = FastAPI()
db_manager = DBSessionManager()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

@app.on_event("startup")
def on_startup():
    # Create database tables
    db_manager.create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)


def main():
    """main function"""
    from engine.dbase import DBSessionManager
    storage = DBSessionManager()
    storage.create_tables()

if __name__ == '__main__':
    main()