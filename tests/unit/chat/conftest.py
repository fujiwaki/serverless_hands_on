"""Shared test fixtures and configurations for domain layer."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from chat.domain.post import AbstractPostRepository, Post
from chat.domain.thread import AbstractThreadRepository, Thread
from chat.shared.exceptions import PostNotFoundError, ThreadNotFoundError

if TYPE_CHECKING:
    from datetime import datetime

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
        if id_ not in self._threads:
            raise ThreadNotFoundError(id_)
        del self._threads[id_]


@pytest.fixture()
def thread_repository() -> InMemoryThreadRepository:
    """Fixture for an in-memory thread repository."""
    return InMemoryThreadRepository()


class InMemoryPostRepository(AbstractPostRepository):
    """In-memory implementation of the AbstractPostRepository interface."""

    def __init__(self) -> None:
        """Initialize the repository."""
        self._posts: dict[ULID, Post] = {}

    def save(self, post: Post) -> None:
        """Save the given Post instance to the repository.

        Args:
            post: The Post instance to be saved.
        """
        self._posts[post.id_] = post

    def list_by_thread_id(self, thread_id: ULID, start: datetime | None = None) -> list[Post]:
        """Find all Post instances by the thread ID.

        Args:
            thread_id: The ULID of the thread to find.
            start: The timestamp to start listing posts from.
        """
        posts = [post for post in self._posts.values() if post.thread_id == thread_id]
        if start:
            posts = [post for post in posts if post.created_at >= start]

        return posts

    def delete(self, id_: ULID) -> None:
        """Delete the post with the given ID.

        Args:
            id_: The ID of the post to delete.
        """
        if id_ not in self._posts:
            raise PostNotFoundError(id_)
        del self._posts[id_]


@pytest.fixture()
def post_repository() -> InMemoryPostRepository:
    """Fixture for an in-memory post repository."""
    return InMemoryPostRepository()
