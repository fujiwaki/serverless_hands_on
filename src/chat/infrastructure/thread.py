"""Repository implementation for Thread entities."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Self

from boto3.dynamodb.conditions import Key
from pydantic import BaseModel
from ulid import ULID

from chat.domain.thread import AbstractThreadRepository, Thread
from chat.shared.exceptions import ThreadNotFoundError

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class ThreadData(BaseModel):
    """Thread data model for DynamoDB record.

    Attributes:
        thread_id: The ID of the thread.
        post_id: The ID of the post.
        category: The category of the record. Always "Thread".
        name: The name of the thread.
        created_at: The timestamp when the thread was created.
    """

    thread_id: str
    post_id: str
    category: str
    name: str
    created_at: int

    @classmethod
    def from_model(cls, model: Thread) -> Self:
        """Create a ThreadData instance from a Thread model.

        Args:
            model: The Thread model to convert.

        Returns:
            The converted ThreadData instance.
        """
        return cls(
            thread_id=str(model.id_),
            post_id="-",
            category="Thread",
            name=model.name,
            created_at=int(model.created_at.timestamp() * 1000000),
        )

    def to_model(self) -> Thread:
        """Convert the ThreadData instance to a Thread model.

        Returns:
            The converted Thread model.
        """
        return Thread(
            id_=ULID.from_str(self.thread_id),
            name=self.name,
            created_at=datetime.fromtimestamp(self.created_at / 1000000, tz=UTC),
        )


class DynamoDBThreadRepository(AbstractThreadRepository):
    """DynamoDB repository for Thread entities."""

    def __init__(self, table: Table) -> None:
        """Initialize the repository.

        Args:
            table: The DynamoDB table to use.
        """
        self._table = table

    def save(self, thread: Thread) -> None:
        """Save the given Thread instance to the repository.

        Args:
            thread: The Thread instance to be saved.
        """
        self._table.put_item(Item=ThreadData.from_model(thread).model_dump(exclude_none=True))

    def find_by_id(self, thread_id: ULID) -> Thread | None:
        """Find a thread by its ID.

        Args:
            thread_id: The ID of the thread to find.

        Returns:
            The Thread instance corresponding to the given ID, or None if not found.
        """
        response = self._table.get_item(Key={"thread_id": str(thread_id), "post_id": "-"})
        item = response.get("Item")
        return ThreadData.model_validate(item).to_model() if item else None

    def list_all(self) -> list[Thread]:
        """List all threads.

        Returns:
            The list of all threads.
        """
        response = self._table.query(IndexName="by_category", KeyConditionExpression=Key("category").eq("Thread"))
        items = response.get("Items", [])
        return [ThreadData.model_validate(item).to_model() for item in items]

    def delete(self, id_: ULID) -> None:
        """Delete the thread with the given ID.

        Args:
            id_: The ID of the thread to delete.
        """
        response = self._table.delete_item(Key={"thread_id": str(id_), "post_id": "-"}, ReturnValues="ALL_OLD")

        if not response.get("Attributes"):
            raise ThreadNotFoundError(id_)
