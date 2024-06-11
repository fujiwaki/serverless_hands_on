"""Use case for deleting posts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # noqa: TCH002

from chat.domain.post import AbstractPostRepository


class DeletePostCommand(BaseModel):
    """Command to delete a post."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

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
        self._repository.delete(command.post_id)
