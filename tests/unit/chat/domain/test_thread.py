"""Unit tests for the Thread models."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from chat.domain.thread import Thread


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
