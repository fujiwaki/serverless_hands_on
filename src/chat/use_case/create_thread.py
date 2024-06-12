"""Use case for creating new threads."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from chat.domain.thread import AbstractThreadRepository, ThreadBuilder

from .dto import ThreadDTO


class CreateThreadCommand(BaseModel):
    """Command to create a new thread.

    Attributes:
        name: The name of the thread.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    name: str


class CreateThread:
    """Use case for creating new threads."""

    def __init__(self, repository: AbstractThreadRepository) -> None:
        """Initialize the use case.

        Args:
            repository: The repository to use for thread operations.
        """
        self._repository = repository

    def execute(self, command: CreateThreadCommand) -> ThreadDTO:
        """Execute the use case.

        Args:
            command: The command to execute.

        Raises:
            ValueError: If the thread name is empty.
            ThreadExistsError: If a thread with the same name already exists.
        """
        thread = ThreadBuilder(self._repository).build(command.name)
        self._repository.save(thread)

        return ThreadDTO.from_model(thread)
