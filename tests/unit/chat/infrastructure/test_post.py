"""Unit tests for the DynamoDBThreadRepository class."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

import pytest
from chat.domain.post import Post
from chat.infrastructure import DynamoDBPostRepository
from chat.shared.exceptions import PostNotFoundError
from ulid import ULID

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class TestDynamoDBPostRepository:
    """Unit tests for the DynamoDBPostRepository class."""

    def test_save_successful(self, table: Table) -> None:
        """Test the save method."""
        repository = DynamoDBPostRepository(table)

        thread_id = "01DXF6DT000000000000000000"
        post_id = "01DXHRTH000000000000000000"
        post = Post(
            id_=post_id,
            thread_id=thread_id,
            message="Message1",
            created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
        )

        repository.save(post)

        actual = table.get_item(Key={"thread_id": thread_id, "post_id": post_id})["Item"]
        expected = {
            "thread_id": thread_id,
            "post_id": post_id,
            "category": "Post",
            "message": "Message1",
            "created_at": Decimal("1577926861000001"),
        }
        assert actual == expected

    def test_save_with_existing_post(self, table: Table) -> None:
        """Test the save method with an existing post."""
        thread_id = "01DXF6DT000000000000000000"
        post_id = "01DXHRTH000000000000000000"
        table.put_item(
            Item={
                "thread_id": thread_id,
                "post_id": post_id,
                "category": "Post",
                "message": "Message1",
                "created_at": Decimal("1577926861000001"),
            }
        )

        repository = DynamoDBPostRepository(table)

        post = Post(
            id_=post_id,
            thread_id=thread_id,
            message="Message2",
            created_at=datetime(2020, 1, 3, 1, 1, 1, 1, tzinfo=UTC),
        )

        repository.save(post)

        actual = table.get_item(Key={"thread_id": thread_id, "post_id": post_id})["Item"]
        expected = {
            "thread_id": thread_id,
            "post_id": post_id,
            "category": "Post",
            "message": "Message2",
            "created_at": Decimal("1578013261000001"),
        }
        assert actual == expected

    def test_list_by_thread_id_successful(self, table: Table) -> None:
        """Test the list_by_thread_id method."""
        thread_id = "01DXF6DT000000000000000000"
        items = [
            {
                "thread_id": thread_id,
                "post_id": "01DXHRTH000000000000000000",
                "category": "Post",
                "message": "Message1",
                "created_at": Decimal("1577926861000001"),
            },
            {
                "thread_id": thread_id,
                "post_id": "01DXMB78000000000000000000",
                "category": "Post",
                "message": "Message2",
                "created_at": Decimal("1578013261000001"),
            },
        ]
        for item in items:
            table.put_item(Item=item)  # type: ignore[arg-type]

        repository = DynamoDBPostRepository(table)

        actual = repository.list_by_thread_id(ULID.from_str(thread_id))
        expected = [
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
        assert actual == expected

    def test_list_by_thread_id_with_no_posts(self, table: Table) -> None:
        """Test the list_by_thread_id method with no posts."""
        repository = DynamoDBPostRepository(table)

        thread_id = "01DXF6DT000000000000000000"
        actual = repository.list_by_thread_id(ULID.from_str(thread_id))

        assert actual == []

    def test_list_by_thread_id_sorted(self, table: Table) -> None:
        """Test the list_by_thread_id method with sorted posts."""
        thread_id = "01DXF6DT000000000000000000"
        items = [
            {
                "thread_id": thread_id,
                "post_id": "01DXMB78000000000000000000",
                "category": "Post",
                "message": "Message2",
                "created_at": Decimal("1578013261000001"),
            },
            {
                "thread_id": thread_id,
                "post_id": "01DXHRTH000000000000000000",
                "category": "Post",
                "message": "Message1",
                "created_at": Decimal("1577926861000001"),
            },
        ]
        for item in items:
            table.put_item(Item=item)  # type: ignore[arg-type]

        repository = DynamoDBPostRepository(table)

        actual = repository.list_by_thread_id(ULID.from_str(thread_id))
        expected = [
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
        assert actual == expected

    def test_list_by_thread_id_with_start(self, table: Table) -> None:
        """Test the list_by_thread_id method with a start parameter."""
        thread_id = "01DXF6DT000000000000000000"
        items = [
            {
                "thread_id": thread_id,
                "post_id": "01DXHRTH000000000000000000",
                "category": "Post",
                "message": "Message1",
                "created_at": Decimal("1577926861000001"),
            },
            {
                "thread_id": thread_id,
                "post_id": "01DXMB78000000000000000000",
                "category": "Post",
                "message": "Message2",
                "created_at": Decimal("1578013261000001"),
            },
        ]
        for item in items:
            table.put_item(Item=item)  # type: ignore[arg-type]

        repository = DynamoDBPostRepository(table)

        actual = repository.list_by_thread_id(ULID.from_str(thread_id), start=datetime(2020, 1, 3, tzinfo=UTC))
        expected = [
            Post(
                id_="01DXMB78000000000000000000",
                thread_id=thread_id,
                message="Message2",
                created_at=datetime(2020, 1, 3, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]
        assert actual == expected

    def test_delete_successful(self, table: Table) -> None:
        """Test the delete method."""
        thread_id = "01DXF6DT000000000000000000"
        post_id = "01DXHRTH000000000000000000"
        table.put_item(
            Item={
                "thread_id": thread_id,
                "post_id": post_id,
                "category": "Post",
                "message": "Message1",
                "created_at": Decimal("1577926861000001"),
            }
        )

        repository = DynamoDBPostRepository(table)

        repository.delete(ULID.from_str(thread_id), ULID.from_str(post_id))

        actual = table.get_item(Key={"thread_id": thread_id, "post_id": post_id}).get("Item")
        assert actual is None

    def test_delete_with_nonexistent_post(self, table: Table) -> None:
        """Test the delete method with a non-existent post."""
        repository = DynamoDBPostRepository(table)

        thread_id = "01DXF6DT000000000000000000"
        post_id = "01DXHRTH000000000000000000"

        with pytest.raises(PostNotFoundError, match=post_id):
            repository.delete(ULID.from_str(thread_id), ULID.from_str(post_id))
