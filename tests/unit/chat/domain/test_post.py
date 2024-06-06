"""Unit tests for the Post models."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest
from chat.domain.post import Post, PostBuilder
from chat.domain.thread import Thread
from chat.shared.exceptions import ThreadNotFoundError
from freezegun import freeze_time
from ulid import ULID

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryThreadRepository


class TestPost:
    """Unit tests for the Post model."""

    def test_init(self) -> None:
        """Test the initialization of a Post instance."""
        id_ = "01DXF6DT000000000000000000"
        thread_id = "01DXHRTH000000000000000000"
        message = "Message"
        created_at = datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC)

        actual = Post(id_=id_, thread_id=thread_id, message=message, created_at=created_at)

        assert actual.id_ == id_
        assert actual.thread_id == thread_id
        assert actual.message == message
        assert actual.created_at == created_at


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
