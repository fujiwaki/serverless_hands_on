"""Unit tests for the CreateThread use case."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest
from chat.domain.thread import Thread
from chat.shared.exceptions import ThreadExistsError
from chat.use_case import CreateThread, CreateThreadCommand, ThreadDTO

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryThreadRepository


class TestCreateThread:
    """Unit tests for the CreateThread use case."""

    def test_execute_successful(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test the successful execution of the use case."""
        command = CreateThreadCommand(name="New Thread")
        use_case = CreateThread(thread_repository)

        actual = use_case.execute(command)

        assert isinstance(actual, ThreadDTO)
        assert actual.name == "New Thread"

    def test_execute_with_existent_thread_name(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test the execution of the use case with an existent thread name."""
        thread = Thread(
            id_="01DXF6DT000000000000000000", name="Thread1", created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC)
        )
        thread_repository.save(thread)

        command = CreateThreadCommand(name="Thread1")
        use_case = CreateThread(thread_repository)

        with pytest.raises(ThreadExistsError, match="Thread1"):
            use_case.execute(command)

    def test_execute_with_empty_thread_name(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test the execution of the use case with an empty thread name."""
        command = CreateThreadCommand(name="")
        use_case = CreateThread(thread_repository)

        with pytest.raises(ValueError, match=r".*empty.*"):
            use_case.execute(command)
