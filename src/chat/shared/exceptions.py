"""Custom exception classes for chat."""

from __future__ import annotations


class ThreadExistsError(Exception):
    """Raised when a thread with the same name already exists."""


class ThreadNotFoundError(Exception):
    """Raised when a thread is not found in the repository."""
