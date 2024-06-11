"""Unit tests for the DeletePost use case."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest
from chat.domain.post import Post
from chat.shared.exceptions import PostNotFoundError
from chat.use_case import DeletePost, DeletePostCommand

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryPostRepository


class TestDeletePost:
    """Unit tests for the DeletePost use case."""

    def test_execute_successful(self, post_repository: InMemoryPostRepository) -> None:
        """Test the execution of the use case."""
        thread_id = "01DXF6DT000000000000000000"
        post = Post(
            id_="01DXHRTH000000000000000000",
            thread_id=thread_id,
            message="Message1",
            created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
        )
        post_repository.save(post)

        command = DeletePostCommand(post_id="01DXHRTH000000000000000000")
        use_case = DeletePost(post_repository)

        use_case.execute(command)

    def test_execute_with_nonexistent_post(self, post_repository: InMemoryPostRepository) -> None:
        """Test the execution of the use case with a non-existent post."""
        post_id = "01DXHRTH000000000000000000"
        command = DeletePostCommand(post_id=post_id)
        use_case = DeletePost(post_repository)

        with pytest.raises(PostNotFoundError):
            use_case.execute(command)
