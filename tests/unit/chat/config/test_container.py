"""Tests for the Container class."""

from __future__ import annotations

from chat.config.container import Container
from chat.infrastructure import DynamoDBPostRepository, DynamoDBThreadRepository
from chat.use_case import CreatePost, CreateThread, DeletePost, DeleteThread, GetThread, ListPosts, ListThreads


class TestConatiner:
    """Tests for the Container class."""

    def test_table(self) -> None:
        """Test that it returns a Table instance."""
        container = Container("table_name")
        table = container.table

        assert table.name == "table_name"

    def test_table_cached(self) -> None:
        """Test that it returns the same Table instance when called multiple times."""
        container = Container("table_name")
        table1 = container.table
        table2 = container.table
        assert table1 is table2

    def test_thread_repository(self) -> None:
        """Test that it returns a DynamoDBThreadRepository instance."""
        container = Container("table_name")
        repository = container.thread_repository

        assert isinstance(repository, DynamoDBThreadRepository)
        assert repository._table.name == "table_name"

    def test_post_repository(self) -> None:
        """Test that it returns a DynamoDBPostRepository instance."""
        container = Container("table_name")
        repository = container.post_repository

        assert isinstance(repository, DynamoDBPostRepository)
        assert repository._table.name == "table_name"

    def test_create_thread(self) -> None:
        """Test that it returns a CreateThread instance."""
        container = Container("table_name")
        use_case = container.create_thread

        assert isinstance(use_case, CreateThread)
        assert isinstance(use_case._repository, DynamoDBThreadRepository)

    def test_get_thread(self) -> None:
        """Test that it returns a GetThread instance."""
        container = Container("table_name")
        use_case = container.get_thread

        assert isinstance(use_case, GetThread)
        assert isinstance(use_case._repository, DynamoDBThreadRepository)

    def test_list_threads(self) -> None:
        """Test that it returns a ListThreads instance."""
        container = Container("table_name")
        use_case = container.list_threads

        assert isinstance(use_case, ListThreads)
        assert isinstance(use_case._repository, DynamoDBThreadRepository)

    def test_delete_thread(self) -> None:
        """Test that it returns a DeleteThread instance."""
        container = Container("table_name")
        use_case = container.delete_thread

        assert isinstance(use_case, DeleteThread)
        assert isinstance(use_case._repository, DynamoDBThreadRepository)

    def test_create_post(self) -> None:
        """Test that it returns a CreatePost instance."""
        container = Container("table_name")
        use_case = container.create_post

        assert isinstance(use_case, CreatePost)
        assert isinstance(use_case._thread_repository, DynamoDBThreadRepository)
        assert isinstance(use_case._post_repository, DynamoDBPostRepository)

    def test_list_posts(self) -> None:
        """Test that it returns a ListPosts instance."""
        container = Container("table_name")
        use_case = container.list_posts

        assert isinstance(use_case, ListPosts)
        assert isinstance(use_case._repository, DynamoDBPostRepository)

    def test_delete_post(self) -> None:
        """Test that it returns a DeletePost instance."""
        container = Container("table_name")
        use_case = container.delete_post

        assert isinstance(use_case, DeletePost)
        assert isinstance(use_case._repository, DynamoDBPostRepository)
