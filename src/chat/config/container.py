"""DI container for the chat application."""

from __future__ import annotations

from typing import TYPE_CHECKING

import boto3

from chat.infrastructure import DynamoDBPostRepository, DynamoDBThreadRepository
from chat.use_case import CreatePost, CreateThread, DeletePost, DeleteThread, GetThread, ListPosts, ListThreads

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class Container:
    """Dependency container for the chat application."""

    def __init__(self, table_name: str) -> None:
        """Initialize the container.

        Args:
            table_name: The name of the DynamoDB table.
        """
        self._table_name = table_name

    @property
    def table(self) -> Table:
        """The DynamoDB table instance."""
        if not hasattr(self, "_table"):
            self._table = boto3.resource("dynamodb").Table(self._table_name)
        return self._table

    @property
    def thread_repository(self) -> DynamoDBThreadRepository:
        """The thread repository instance."""
        if not hasattr(self, "_thread_repository"):
            self._thread_repository = DynamoDBThreadRepository(self.table)
        return self._thread_repository

    @property
    def post_repository(self) -> DynamoDBPostRepository:
        """The post repository instance."""
        if not hasattr(self, "_post_repository"):
            self._post_repository = DynamoDBPostRepository(self.table)
        return self._post_repository

    @property
    def create_thread(self) -> CreateThread:
        """The create thread use case instance."""
        if not hasattr(self, "_create_thread"):
            self._create_thread = CreateThread(self.thread_repository)
        return self._create_thread

    @property
    def get_thread(self) -> GetThread:
        """The get thread use case instance."""
        if not hasattr(self, "_get_thread"):
            self._get_thread = GetThread(self.thread_repository)
        return self._get_thread

    @property
    def list_threads(self) -> ListThreads:
        """The list threads use case instance."""
        if not hasattr(self, "_list_threads"):
            self._list_threads = ListThreads(self.thread_repository)
        return self._list_threads

    @property
    def delete_thread(self) -> DeleteThread:
        """The delete thread use case instance."""
        if not hasattr(self, "_delete_thread"):
            self._delete_thread = DeleteThread(self.thread_repository)
        return self._delete_thread

    @property
    def create_post(self) -> CreatePost:
        """The create post use case instance."""
        if not hasattr(self, "_create_post"):
            self._create_post = CreatePost(self.thread_repository, self.post_repository)
        return self._create_post

    @property
    def list_posts(self) -> ListPosts:
        """The list posts use case instance."""
        if not hasattr(self, "_list_posts"):
            self._list_posts = ListPosts(self.post_repository)
        return self._list_posts

    @property
    def delete_post(self) -> DeletePost:
        """The delete post use case instance."""
        if not hasattr(self, "_delete_post"):
            self._delete_post = DeletePost(self.post_repository)
        return self._delete_post
