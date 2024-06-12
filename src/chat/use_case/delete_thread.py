"""Use case for deleting threads."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # noqa: TCH002

if TYPE_CHECKING:
    from chat.domain.thread import AbstractThreadRepository


class DeleteThreadCommand(BaseModel):
    """Command to delete a thread.

    Attributes:
        thread_id: The ID of the thread to delete.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    thread_id: ULID


class DeleteThread:
    """Use case for deleting threads."""

    def __init__(self, repository: AbstractThreadRepository) -> None:
        """Initialize the use case.

        Args:
            repository: The repository to use for thread operations.
        """
        self._repository = repository

    def execute(self, command: DeleteThreadCommand) -> None:
        """Execute the use case.

        Args:
            command: The command to execute.

        Raises:
            ThreadNotFoundError: If the thread with the given ID does not exist.
        """
        self._repository.delete(command.thread_id)
