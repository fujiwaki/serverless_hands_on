"""Use case for getting thread."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel
from ulid import ULID  # noqa: TCH002

from .dto import ThreadDTO

if TYPE_CHECKING:
    from chat.domain.thread import AbstractThreadRepository


class GetThreadCommand(BaseModel):
    """Command to get a thread.

    Attributes:
        thread_id: The ID of the thread to get.
    """

    thread_id: ULID


class GetThread:
    """Use case for getting thread."""

    def __init__(self, repository: AbstractThreadRepository) -> None:
        """Initialize the use case.

        Args:
            repository: The repository to use for thread operations.
        """
        self._repository = repository

    def execute(self, command: GetThreadCommand) -> ThreadDTO | None:
        """Execute the use case.

        Returns:
            The thread if found, otherwise None.
        """
        thread = self._repository.find_by_id(command.thread_id)
        return ThreadDTO.from_model(thread) if thread else None
