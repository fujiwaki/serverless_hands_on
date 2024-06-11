"""Use case for getting posts."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # noqa: TCH002

from .dto import PostDTO

if TYPE_CHECKING:
    from chat.domain.post import AbstractPostRepository


class GetPostsCommand(BaseModel):
    """Command to get posts."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    thread_id: ULID
    start_time: datetime | None = None


class GetPosts:
    """Use case for getting posts.

    This use case retrieves posts from a specific thread identified by the thread_id.
    The posts are sorted by their creation time.
    """

    def __init__(self, repository: AbstractPostRepository) -> None:
        """Initialize the use case.

        Args:
            repository: The repository to use for post operations.
        """
        self._repository = repository

    def execute(self, command: GetPostsCommand) -> list[PostDTO]:
        """Execute the use case.

        Args:
            command: The command to execute.

        Returns:
            The list of posts.
        """
        posts = self._repository.list_by_thread_id(command.thread_id, start=command.start_time)
        posts.sort(key=lambda x: x.created_at)

        return [PostDTO.from_model(post) for post in posts]
