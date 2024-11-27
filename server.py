#!/usr/bin/env python3
"""a crime tracker server"""
from fastapi import FastAPI
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://eyewitness.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)





