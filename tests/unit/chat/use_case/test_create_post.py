"""Unit tests for the CreatePost use case."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest
from chat.domain.thread import Thread
from chat.shared.exceptions import ThreadNotFoundError
from chat.use_case import CreatePost, CreatePostCommand

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryPostRepository, InMemoryThreadRepository


class TestCreatePost:
    """Unit tests for the CreatePost use case."""

    def test_execute_successful(
        self, thread_repository: InMemoryThreadRepository, post_repository: InMemoryPostRepository
    ) -> None:
        """Test the successful execution of the use case."""
        thread_id = "01DXF6DT000000000000000000"
        thread = Thread(id_=thread_id, name="Thread1", created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC))
        thread_repository.save(thread)

        command = CreatePostCommand(thread_id="01DXF6DT000000000000000000", message="New Message")
        use_case = CreatePost(thread_repository, post_repository)

        use_case.execute(command)

    def test_execute_with_nonexistent_thread(
        self, thread_repository: InMemoryThreadRepository, post_repository: InMemoryPostRepository
    ) -> None:
        """Test the execution of the use case with a non-existent thread."""
        command = CreatePostCommand(thread_id="01DXF6DT000000000000000000", message="New Message")
        use_case = CreatePost(thread_repository, post_repository)

        with pytest.raises(ThreadNotFoundError):
            use_case.execute(command)

    def test_execute_with_empty_message(
        self, thread_repository: InMemoryThreadRepository, post_repository: InMemoryPostRepository
    ) -> None:
        """Test the execution of the use case with an empty message."""
        thread_id = "01DXF6DT000000000000000000"
        thread = Thread(id_=thread_id, name="Thread1", created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC))
        thread_repository.save(thread)

        command = CreatePostCommand(thread_id="01DXF6DT000000000000000000", message="")
        use_case = CreatePost(thread_repository, post_repository)

        with pytest.raises(ValueError, match=r".*empty.*"):
            use_case.execute(command)
