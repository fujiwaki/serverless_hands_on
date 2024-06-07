"""Unit tests for the DeleteThread use case."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest
from chat.domain.thread import Thread
from chat.shared.exceptions import ThreadNotFoundError
from chat.use_case import DeleteThread, DeleteThreadCommand

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryThreadRepository


class TestDeleteThread:
    """Unit tests for the DeleteThread use case."""

    def test_execute_successful(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test the successful execution of the use case."""
        thread = Thread(
            id_="01DXF6DT000000000000000000", name="Thread1", created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC)
        )
        thread_repository.save(thread)

        command = DeleteThreadCommand(thread_id="01DXF6DT000000000000000000")
        use_case = DeleteThread(thread_repository)

        use_case.execute(command)

    def test_execute_with_nonexistent_thread(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test the execution of the use case with a non-existent thread."""
        thread_id = "01DXF6DT000000000000000000"
        command = DeleteThreadCommand(thread_id=thread_id)
        use_case = DeleteThread(thread_repository)

        with pytest.raises(ThreadNotFoundError):
            use_case.execute(command)
