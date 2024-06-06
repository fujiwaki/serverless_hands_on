""""""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, field_validator
from ulid import ULID

from chat.shared.exceptions import ThreadNotFoundError

if TYPE_CHECKING:
    from chat.domain.thread import AbstractThreadRepository


class Post(BaseModel):
    """Post model.

    Attributes:
        id_: The ID of the post.
        thread_id: The ID of the thread that the post belongs to.
        message: The message of the post.
        created_at: The timestamp when the post was created, in UTC.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    id_: ULID
    thread_id: ULID
    message: str
    created_at: datetime

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, message: str) -> str:
        """Validate that the message is not empty."""
        if not message:
            error_message = "The message must not be empty."
            raise ValueError(error_message)
        return message


class AbstractPostRepository(ABC):
    """Defines the interface for a post repository."""

    @abstractmethod
    def save(self, post: Post) -> None:
        """Save the given Post instance to the repository.

        Args:
            post: The Post instance to be saved.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_thread_id(self, thread_id: ULID) -> list[Post]:
        """Find all Post instances by the thread ID.

        Args:
            thread_id: The ULID of the thread to find.

        Returns:
            A list of Post instances with the specified thread ID.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id_: ULID) -> None:
        """Delete a Post instance by its ID.

        Args:
            id_: The ULID of the post to delete.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError


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
