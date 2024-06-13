"""Domain builders for the chat module."""

from __future__ import annotations

from datetime import UTC, datetime

from ulid import ULID

from chat.shared.exceptions import ThreadExistsError, ThreadNotFoundError

from .post import Post
from .thread import AbstractThreadRepository, Thread


class ThreadBuilder:
    """Builder for the Thread model."""

    def __init__(self, repository: AbstractThreadRepository) -> None:
        """Initialize the ThreadBuilder instance.

        Args:
            repository: The repository to use for thread operations.
        """
        self._repository = repository

    def build(self, name: str) -> Thread:
        """Build the Thread instance.

        Args:
            name: The name of the thread.

        Returns:
            The built Thread instance.

        Raises:
            ThreadExistsError: If a thread with the given name already exists.
        """
        threads = self._repository.list_all()
        if any(thread.name == name for thread in threads):
            raise ThreadExistsError(name)
        return Thread(id_=ULID(), name=name, created_at=datetime.now(tz=UTC))


class PostBuilder:
    """Builder for the Post model."""

    def __init__(self, repository: AbstractThreadRepository) -> None:
        """Initialize the PostBuilder instance."""
        self._repository = repository

    def build(self, thread_id: ULID, message: str) -> Post:
        """Build the Post instance.

        Args:
            thread_id: The ID of the thread that the post belongs to.
            message: The message of the post.
        """
        if not self._repository.find_by_id(thread_id):
            raise ThreadNotFoundError(thread_id)

        return Post(id_=ULID(), thread_id=thread_id, message=message, created_at=datetime.now(tz=UTC))
