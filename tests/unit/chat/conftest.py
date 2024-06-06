"""Shared test fixtures and configurations for domain layer."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from src.chat.domain.thread import AbstractThreadRepository, Thread

if TYPE_CHECKING:
    from ulid import ULID


class InMemoryThreadRepository(AbstractThreadRepository):
    """In-memory implementation of the AbstractThreadRepository interface."""

    def __init__(self) -> None:
        """Initialize the repository."""
        self._threads: dict[ULID, Thread] = {}

    def save(self, thread: Thread) -> None:
        """Save the given Thread instance to the repository.

        Args:
            thread: The Thread instance to be saved.
        """
        self._threads[thread.id_] = thread

    def find_by_id(self, thread_id: ULID) -> Thread | None:
        """Find a Thread instance by its ID.

        Args:
            thread_id: The ULID of the thread to find.
        """
        return self._threads.get(thread_id)

    def list_all(self) -> list[Thread]:
        """Retrieves a list of all threads."""
        return list(self._threads.values())

    def delete(self, id_: ULID) -> None:
        """Delete the thread with the given ID.

        Args:
            id_: The ID of the thread to delete.
        """
        del self._threads[id_]


@pytest.fixture()
def thread_repository() -> InMemoryThreadRepository:
    """Fixture for an in-memory thread repository."""
    return InMemoryThreadRepository()
