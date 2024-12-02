#!/usr/bin/python3
"""a module for crime entity"""
import enum


class CrimeCategory(enum.Enum):
    THEFT = "Theft"
    ASSAULT = "Assault"
    VANDALISM = "Vandalism"
    FRAUD = "Fraud"
    OTHER = "Other"