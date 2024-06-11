"""Unit tests for the GetThreads use case."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from chat.domain.thread import Thread
from chat.use_case import GetThreads, ThreadDTO

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryThreadRepository


class TestGetThreads:
    """Unit tests for the GetThreads use case."""

    def test_execute_successful(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test the successful execution of the use case."""
        threads = [
            Thread(
                id_="01DXF6DT000000000000000000",
                name="Thread1",
                created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC),
            ),
            Thread(
                id_="01DXHRTH000000000000000000",
                name="Thread2",
                created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]
        for thread in threads:
            thread_repository.save(thread)

        actual = GetThreads(thread_repository).execute()

        expected = [
            ThreadDTO(
                id_="01DXF6DT000000000000000000",
                name="Thread1",
                created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC),
            ),
            ThreadDTO(
                id_="01DXHRTH000000000000000000",
                name="Thread2",
                created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]

        assert actual == expected

    def test_execute_with_no_threads(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test the execution of the use case with no threads."""
        actual = GetThreads(thread_repository).execute()

        assert actual == []
