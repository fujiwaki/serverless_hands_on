"""Use case for creating new posts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # noqa: TCH002

from chat.domain.post import AbstractPostRepository, PostBuilder

if TYPE_CHECKING:
    from chat.domain.thread import AbstractThreadRepository


class CreatePostCommand(BaseModel):
    """Command to create a new post."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    thread_id: ULID
    message: str


class CreatePost:
    """Use case for creating new posts."""

    def __init__(self, thread_repository: AbstractThreadRepository, post_repository: AbstractPostRepository) -> None:
        """Initialize the use case.

        Args:
            thread_repository:
        """
        self._thread_repository = thread_repository
        self._post_repository = post_repository

    def execute(self, command: CreatePostCommand) -> None:
        """Execute the use case.

        Args:
            command: The command to execute.

        Raises:
            ThreadNotFoundError: If the thread with the given ID does not exist.
        """
        post = PostBuilder(self._thread_repository).build(command.thread_id, command.message)
        self._post_repository.save(post)
