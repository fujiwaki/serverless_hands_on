"""Thread repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ulid import ULID

    from chat.domain.thread.models import Thread


class AbstractThreadRepository(ABC):
    """Abstract Thread repository."""

    @abstractmethod
    def save(self, thread: Thread) -> None:
        """Save thread."""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, thread_id: ULID) -> Thread:
        """Find thread by id."""
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Thread]:
        """List all threads."""
        raise NotImplementedError
