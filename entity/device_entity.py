#!/usr/bin/python3
"""a module for device entity"""
import enum

class DeviceType(enum.Enum):
    MOBILE = "Mobile"
    DESKTOP = "Desktop"
    TABLET = "Tablet"
    OTHER = "Other"