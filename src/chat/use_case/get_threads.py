"""Use case for getting threads."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .dto import ThreadDTO

if TYPE_CHECKING:
    from chat.domain.thread import AbstractThreadRepository


class GetThreads:
    """Use case for getting threads."""

    def __init__(self, repository: AbstractThreadRepository) -> None:
        """Initialize the use case.

        Args:
            repository: The repository to use for thread operations.
        """
        self._repository = repository

    def execute(self) -> list[ThreadDTO]:
        """Execute the use case.

        Returns:
            The list of threads.
        """
        threads = self._repository.list_all()
        threads.sort(key=lambda x: x.id_)
        return [ThreadDTO.from_model(thread) for thread in threads]
