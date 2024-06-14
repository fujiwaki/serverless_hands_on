"""Unit tests for the GetThread use case."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from chat.domain.thread import Thread
from chat.use_case import GetThread, GetThreadCommand, ThreadDTO

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryThreadRepository


class TestGetThread:
    """Unit tests for the GetThread use case."""

    def test_execute_successful(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test the execution of the use case to get a thread."""
        thread_id = "01DXF6DT000000000000000000"
        thread = Thread(id_=thread_id, name="Test Thread", created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC))
        thread_repository.save(thread)

        command = GetThreadCommand(thread_id=thread_id)
        use_case = GetThread(thread_repository)

        actual = use_case.execute(command)
        expected = ThreadDTO(id_=thread_id, name="Test Thread", created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC))

        assert actual == expected

    def test_execute_with_no_thread(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test the execution of the use case to get a thread that does not exist."""
        command = GetThreadCommand(thread_id="01DXF6DT000000000000000000")
        use_case = GetThread(thread_repository)

        actual = use_case.execute(command)

        assert actual is None
