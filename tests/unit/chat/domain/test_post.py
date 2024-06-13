"""Unit tests for the Post models."""

from __future__ import annotations

from datetime import UTC, datetime

from chat.domain.post import Post


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
