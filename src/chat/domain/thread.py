"""This module defines the Thread models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime  # noqa: TCH003

from pydantic import BaseModel, ConfigDict, field_validator
from ulid import ULID  # noqa: TCH002


class Thread(BaseModel):
    """Thread model.

    Attributes:
        id_: The ID of the thread.
        name: The name of the thread.
        created_at: The timestamp when the thread was created, in UTC.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    id_: ULID
    name: str
    created_at: datetime

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, name: str) -> str:
        """Validate that the name is not empty.

        Args:
            name: The name to validate.

        Returns:
            The name if it is not empty.

        Raises:
            ValueError: If the name is empty.
        """
        if not name:
            error_message = "The thread name must not be empty."
            raise ValueError(error_message)
        return name


class AbstractThreadRepository(ABC):
    """Defines the interface for a thread repository."""

    @abstractmethod
    def save(self, thread: Thread) -> None:
        """Save the given Thread instance to the repository.

        Args:
            thread: The Thread instance to be saved.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, thread_id: ULID) -> Thread | None:
        """Find a Thread instance by its ID.

        Args:
            thread_id: The ULID of the thread to find.

        Returns:
            The Thread instance corresponding to the given ULID.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Thread]:
        """Retrieves a list of all threads.

        Returns:
            A list of Thread objects representing all threads.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, id_: ULID) -> None:
        """Delete the thread with the given ID.

        Args:
            id_: The ID of the thread to delete.

        Raises:
            ThreadNotFoundError: If the thread with the given ID does not exist.
        """
        raise NotImplementedError
