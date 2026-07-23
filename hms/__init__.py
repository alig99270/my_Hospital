"""
Hospital Management System (HMS) - Main Package.

This package provides the core functionality for managing hospital operations
including appointments, medical records, prescriptions, and notifications.
"""
# This ensures the Celery app is always imported when Django starts.
from .celery import app as celery_app

__all__ = ('celery_app',)
