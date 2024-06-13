"""This module defines the Post model and related classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime  # noqa: TCH003

from pydantic import BaseModel, ConfigDict, field_validator
from ulid import ULID  # noqa: TCH002


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
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_thread_id(self, thread_id: ULID, *, start: datetime | None = None) -> list[Post]:
        """List all posts with the specified thread ID.

        This method retrieves a list of Post instances that belong to the specified thread ID.
        The posts are listed starting from the specified timestamp.

        Args:
            thread_id: The ULID of the thread to find.
            start: The timestamp to start listing posts from.

        Returns:
            A list of Post instances with the specified thread ID.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, thread_id: ULID, post_id: ULID) -> None:
        """Delete the Post with the given ID.

        Args:
            thread_id: The ID of the thread that the post belongs to.
            post_id: The ID of the post to delete.

        Raises:
            PostNotFoundError: If the post with the given ID does not exist.
        """
        raise NotImplementedError
