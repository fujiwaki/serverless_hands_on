"""DTOs for chat use case."""

from __future__ import annotations

from datetime import datetime  # noqa: TCH003
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # noqa: TCH002

if TYPE_CHECKING:
    from chat.domain.post import Post
    from chat.domain.thread import Thread


class DTOBase(BaseModel):
    """Base class for DTOs."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class ThreadDTO(DTOBase):
    """DTO for thread.

    Attributes:
        id_: The ID of the thread.
        name: The name of the thread.
        created_at: The timestamp when the thread was created.
    """

    id_: ULID
    name: str
    created_at: datetime

    @classmethod
    def from_model(cls, model: Thread) -> Self:
        """Convert a Thread model to a ThreadDTO instance.

        Args:
            model: The Thread model to convert.

        Returns:
            The converted ThreadDTO instance.
        """
        return cls(id_=model.id_, name=model.name, created_at=model.created_at)


class PostDTO(DTOBase):
    """DTO for post.

    Attributes:
        id_: The ID of the post.
        thread_id: The ID of the thread to which the post belongs.
        message: The message of the post.
        created_at: The timestamp when the post was created.
    """

    id_: ULID
    thread_id: ULID
    message: str
    created_at: datetime

    @classmethod
    def from_model(cls, model: Post) -> Self:
        """Convert a Post model to a PostDTO instance.

        Args:
            model: The Post model to convert.

        Returns:
            The converted PostDTO instance.
        """
        return cls(id_=model.id_, thread_id=model.thread_id, message=model.message, created_at=model.created_at)
