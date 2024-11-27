#!/usr/bin/python3
"""a module for storage"""
from engine.dbase import DBSession

storage = DBSession('crime.db')
storage.reload()