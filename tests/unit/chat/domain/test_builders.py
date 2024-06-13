"""Unit tests for the builders in the chat domain."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest
from chat.domain.builders import PostBuilder, ThreadBuilder
from chat.domain.thread import Thread
from chat.shared.exceptions import ThreadExistsError, ThreadNotFoundError
from freezegun import freeze_time
from ulid import ULID

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryThreadRepository


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


class TestPostBuilder:
    """Unit tests for the PostBuilder."""

    @freeze_time("2020-01-01T01:01:01.100000Z")
    def test_build_with_existing_thread(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test building a post with an existing thread."""
        thread = Thread(
            id_="01DXF6DT000000000000000000",
            name="Test Thread",
            created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC),
        )
        thread_repository.save(thread)

        builder = PostBuilder(thread_repository)

        thread_id = thread.id_
        message = "New Message"

        actual = builder.build(thread_id=thread_id, message=message)

        expected_timestamp = datetime(2020, 1, 1, 1, 1, 1, 100000, tzinfo=UTC).timestamp()
        assert actual.id_.timestamp == expected_timestamp
        assert actual.thread_id == thread_id
        assert actual.message == message
        assert actual.created_at.timestamp() == expected_timestamp

    def test_build_with_nonexistent_thread(self, thread_repository: InMemoryThreadRepository) -> None:
        """Test building a post with a nonexistent thread."""
        builder = PostBuilder(thread_repository)

        thread_id = ULID.from_str("01DXHRTH000000000000000000")
        message = "New Message"

        with pytest.raises(ThreadNotFoundError):
            builder.build(thread_id=thread_id, message=message)
