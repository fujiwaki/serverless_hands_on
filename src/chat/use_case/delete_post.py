"""Use case for deleting posts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # noqa: TCH002

if TYPE_CHECKING:
    from chat.domain.post import AbstractPostRepository


class DeletePostCommand(BaseModel):
    """Command to delete a post.

    Attributes:
        thread_id: The ID of the thread that the post belongs to.
        post_id: The ID of the post to delete.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    thread_id: ULID
    post_id: ULID


class DeletePost:
    """Use case for deleting posts."""

    def __init__(self, repository: AbstractPostRepository) -> None:
        """Initialize the use case.

        Args:
            repository: The repository to use for post operations.
        """
        self._repository = repository

    def execute(self, command: DeletePostCommand) -> None:
        """Execute the use case.

        Args:
            command: The command to execute.

        Raises:
            PostNotFoundError: If the post with the given ID does not exist.
        """
        self._repository.delete(command.thread_id, command.post_id)
