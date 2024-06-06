"""Unit tests for the Thread models."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest
from chat.domain.thread import Thread, ThreadBuilder
from chat.shared.exceptions import ThreadExistsError
from freezegun import freeze_time

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryThreadRepository


class TestThread:
    """Unit tests for the Thread model."""

    def test_init_with_valid_name(self) -> None:
        """Test the initialization of a Thread instance with a valid name."""
        id_ = "01DXF6DT000000000000000000"
        name = "Test Thread"
        created_at = datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC)

        actual = Thread(id_=id_, name=name, created_at=created_at)

        assert actual.id_ == id_
        assert actual.name == name
        assert actual.created_at == created_at

    def test_init_with_empty_name(self) -> None:
        """Test the initialization of a Thread instance with an empty name."""
        id_ = "01DXF6DT000000000000000000"
        name = ""
        created_at = datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC)
        with pytest.raises(ValueError, match=r".*empty.*"):
            Thread(id_=id_, name=name, created_at=created_at)


class TestThreadBuilder:
    """Unit tests for the ThreadBuilder."""

    @freeze_time("2020-01-01T01:01:01.100000Z")
    def test_build_with_nonexistent_thread_name(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test building a thread with a nonexistent name."""
        thread = Thread(
            id_="01DXF6DT000000000000000000",
            name="Thread1",
            created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC),
        )
        thread_repository.save(thread)

        builder = ThreadBuilder(thread_repository)
        name = "Thread2"

        actual = builder.build(name=name)

        expected_timestamp = datetime(2020, 1, 1, 1, 1, 1, 100000, tzinfo=UTC).timestamp()
        assert actual.id_.timestamp == expected_timestamp
        assert actual.name == name
        assert actual.created_at.timestamp() == expected_timestamp

    def test_build_with_existing_thread_name(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test building a thread with an existing name."""
        thread = Thread(
            id_="01DXF6DT000000000000000000",
            name="Thread1",
            created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC),
        )
        thread_repository.save(thread)

        builder = ThreadBuilder(thread_repository)
        name = "Thread1"

        with pytest.raises(ThreadExistsError, match="Thread1"):
            builder.build(name=name)
