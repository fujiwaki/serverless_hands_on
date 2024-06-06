"""Use case for creating new threads."""

from __future__ import annotations

from chat.domain.thread import AbstractThreadRepository, ThreadBuilder


class CreateThreadCommand:
    """Command to create a new thread."""

    def __init__(self, name: str) -> None:
        """Initialize the command.

        Args:
            name: The name of the thread to create.
        """
        self.name = name


class CreateThread:
    """Use case for creating new threads."""

    def __init__(self, repository: AbstractThreadRepository) -> None:
        """Initialize the use case.

        Args:
            repository: The repository to use for thread operations.
        """
        self._repository = repository

    def execute(self, command: CreateThreadCommand) -> None:
        """Execute the use case.

        Args:
            command: The command to execute.
        """
        thread = ThreadBuilder(self._repository).build(command.name)
        self._repository.save(thread)
