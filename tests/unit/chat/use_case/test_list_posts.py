"""Unit tests for the ListPosts use case."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from chat.domain.post import Post
from chat.use_case import ListPosts, ListPostsCommand, PostDTO

if TYPE_CHECKING:
    from tests.unit.chat.conftest import InMemoryPostRepository


class TestListPosts:
    """Unit tests for the GetPosts use case."""

    def test_execute_with_all_posts(self, post_repository: InMemoryPostRepository) -> None:
        """Test the execution of the use case to get all posts."""
        thread_id = "01DXF6DT000000000000000000"
        posts = [
            Post(
                id_="01DXHRTH000000000000000000",
                thread_id=thread_id,
                message="Message1",
                created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
            ),
            Post(
                id_="01DXMB78000000000000000000",
                thread_id=thread_id,
                message="Message2",
                created_at=datetime(2020, 1, 3, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]
        for post in posts:
            post_repository.save(post)

        command = ListPostsCommand(thread_id=thread_id)
        use_case = ListPosts(post_repository)

        actual = use_case.execute(command)

        expected = [
            PostDTO(
                id_="01DXHRTH000000000000000000",
                thread_id=thread_id,
                message="Message1",
                created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
            ),
            PostDTO(
                id_="01DXMB78000000000000000000",
                thread_id=thread_id,
                message="Message2",
                created_at=datetime(2020, 1, 3, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]

        assert actual == expected

    def test_execute_with_no_posts(self, post_repository: InMemoryPostRepository) -> None:
        """Test the execution of the use case with no posts."""
        command = ListPostsCommand(thread_id="01DXF6DT000000000000000000")
        use_case = ListPosts(post_repository)

        actual = use_case.execute(command)

        assert actual == []

    def test_execute_sorts_posts_by_creation_time(self, post_repository: InMemoryPostRepository) -> None:
        """Test the execution of the use case with posts sorted by creation time."""
        thread_id = "01DXF6DT000000000000000000"
        posts = [
            Post(
                id_="01DXMB78000000000000000000",
                thread_id=thread_id,
                message="Message2",
                created_at=datetime(2020, 1, 3, 1, 1, 1, 1, tzinfo=UTC),
            ),
            Post(
                id_="01DXHRTH000000000000000000",
                thread_id=thread_id,
                message="Message1",
                created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]
        for post in posts:
            post_repository.save(post)

        command = ListPostsCommand(thread_id=thread_id)
        use_case = ListPosts(post_repository)

        actual = use_case.execute(command)

        expected = [
            PostDTO(
                id_="01DXHRTH000000000000000000",
                thread_id=thread_id,
                message="Message1",
                created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
            ),
            PostDTO(
                id_="01DXMB78000000000000000000",
                thread_id=thread_id,
                message="Message2",
                created_at=datetime(2020, 1, 3, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]

        assert actual == expected

    def test_execute_with_start_time(self, post_repository: InMemoryPostRepository) -> None:
        """Test the execution of the use case with a start time."""
        thread_id = "01DXF6DT000000000000000000"
        posts = [
            Post(
                id_="01DXHRTH000000000000000000",
                thread_id=thread_id,
                message="Message1",
                created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
            ),
            Post(
                id_="01DXMB78000000000000000000",
                thread_id=thread_id,
                message="Message2",
                created_at=datetime(2020, 1, 3, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]
        for post in posts:
            post_repository.save(post)

        command = ListPostsCommand(thread_id=thread_id, start_time=datetime(2020, 1, 3, tzinfo=UTC))
        use_case = ListPosts(post_repository)

        actual = use_case.execute(command)

        expected = [
            PostDTO(
                id_="01DXMB78000000000000000000",
                thread_id=thread_id,
                message="Message2",
                created_at=datetime(2020, 1, 3, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]

        assert actual == expected

    def test_execute_with_start_time_no_posts(self, post_repository: InMemoryPostRepository) -> None:
        """Test the execution of the use case with a start time and no posts."""
        thread_id = "01DXF6DT000000000000000000"
        posts = [
            Post(
                id_="01DXHRTH000000000000000000",
                thread_id=thread_id,
                message="Message1",
                created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
            ),
            Post(
                id_="01DXMB78000000000000000000",
                thread_id=thread_id,
                message="Message2",
                created_at=datetime(2020, 1, 3, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]
        for post in posts:
            post_repository.save(post)

        command = ListPostsCommand(thread_id=thread_id, start_time=datetime(2020, 1, 4, tzinfo=UTC))
        use_case = ListPosts(post_repository)

        actual = use_case.execute(command)

        assert actual == []
