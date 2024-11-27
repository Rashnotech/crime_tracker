#!/usr/bin/env python3
"""a crime tracker server"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
]

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
    pass

if __name__ == '__main__':
    main()