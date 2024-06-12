"""Post repository implementation."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from boto3.dynamodb.conditions import Key
from pydantic import BaseModel
from ulid import ULID

from chat.domain.post import AbstractPostRepository, Post
from chat.shared.exceptions import PostNotFoundError

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class PostData(BaseModel):
    """Post data model for DynamoDB record.

    Attributes:
        thread_id: The ID of the thread.
        post_id: The ID of the post.
        category: The category of the record. Always "Post".
        message: The message of the post.
        created_at: The timestamp when the post was created.
    """

    thread_id: str
    post_id: str
    category: str
    message: str
    created_at: int

    @classmethod
    def from_model(cls, model: Post) -> PostData:
        """Create a PostData instance from a Post model.

        Args:
            model: The Post model to convert.

        Returns:
            The converted PostData instance.
        """
        return cls(
            thread_id=str(model.thread_id),
            post_id=str(model.id_),
            category="Post",
            message=model.message,
            created_at=int(model.created_at.timestamp() * 1000000),
        )

    def to_model(self) -> Post:
        """Convert the PostData instance to a Post model.

        Returns:
            The converted Post model.
        """
        return Post(
            id_=ULID.from_str(self.post_id),
            thread_id=ULID.from_str(self.thread_id),
            message=self.message,
            created_at=datetime.fromtimestamp(self.created_at / 1000000, tz=UTC),
        )


class DynamoDBPostRepository(AbstractPostRepository):
    """DynamoDB repository for Post entities."""

    def __init__(self, table: Table) -> None:
        """Initialize the repository.

        Args:
            table: The DynamoDB table instance.
        """
        self._table = table

    def save(self, post: Post) -> None:
        """Save the given Post instance to the repository.

        Args:
            post: The Post instance to be saved.
        """
        self._table.put_item(Item=PostData.from_model(post).model_dump(exclude_none=True))

    def list_by_thread_id(self, thread_id: ULID, *, start: datetime | None = None) -> list[Post]:
        """List all posts with the specified thread ID.

        Args:
            thread_id: The ID of the thread to find.
            start: The timestamp to start listing posts from.

        Returns:
            A list of Post instances with the specified thread ID.
        """
        key_condition = Key("thread_id").eq(str(thread_id))
        if start:
            key_condition = key_condition & Key("post_id").gt(str(ULID.from_datetime(start))[:10])  # type: ignore[assignment]

        response = self._table.query(KeyConditionExpression=key_condition)
        items = response.get("Items", [])
        return [PostData.model_validate(item).to_model() for item in items]

    def delete(self, thread_id: ULID, post_id: ULID) -> None:
        """Delete the post with the specified ID.

        Args:
            thread_id: The ID of the thread that the post belongs to.
            post_id: The ID of the post to delete.
        """
        response = self._table.delete_item(
            Key={"thread_id": str(thread_id), "post_id": str(post_id)}, ReturnValues="ALL_OLD"
        )

        if not response.get("Attributes"):
            raise PostNotFoundError(post_id)
