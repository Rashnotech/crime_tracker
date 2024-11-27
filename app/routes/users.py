#!/usr/bin/env python3
"""a module for user routes"""
from fastapi import APIRouter


router = APIRouter()

@router.get("/users", tags=["users"])
async def get_users():
    """a route to get all users"""
    return [{"message": "get all users"}]