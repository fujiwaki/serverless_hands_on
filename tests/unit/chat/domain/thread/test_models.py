"""Tests for models."""

from __future__ import annotations

from datetime import UTC, datetime

from freezegun import freeze_time

from src.chat.domain.thread.models import Thread


class TestThread:
    """Test Thread model."""

    def test_init(self) -> None:
        """Test init method."""
        id_ = "01DXF6DT000000000000000000"
        name = "Test Thread"
        created_at = datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC)

        actual = Thread(id_=id_, name=name, created_at=created_at)

        assert actual.id_ == id_
        assert actual.name == name
        assert actual.created_at == created_at

    @freeze_time("2020-01-01T01:01:01.100000Z")
    def test_new(self) -> None:
        """Test new method."""
        name = "Test Thread"

        actual = Thread.new(name)

        expected_timestamp = datetime(2020, 1, 1, 1, 1, 1, 100000, tzinfo=UTC).timestamp()

        assert actual.id_.timestamp == expected_timestamp
        assert actual.name == name
        assert actual.created_at.timestamp() == expected_timestamp
