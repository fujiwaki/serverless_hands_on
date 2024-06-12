"""Unit tests for the DynamoDBThreadRepository class."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

import pytest
from chat.domain.thread import Thread
from chat.infrastructure import DynamoDBThreadRepository
from chat.shared.exceptions import ThreadNotFoundError
from ulid import ULID

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class TestDynamoDBThreadRepository:
    """Unit tests for the DynamoDBThreadRepository class."""

    def test_save_successful(self, table: Table) -> None:
        """Test the save method."""
        repository = DynamoDBThreadRepository(table)

        thread = Thread(
            id_="01DXF6DT000000000000000000",
            name="Test Thread",
            created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC),
        )

        repository.save(thread)

        actual = table.get_item(Key={"thread_id": "01DXF6DT000000000000000000", "post_id": "-"})["Item"]
        expected = {
            "thread_id": "01DXF6DT000000000000000000",
            "post_id": "-",
            "category": "Thread",
            "name": "Test Thread",
            "created_at": Decimal("1577840461000001"),
        }

        assert actual == expected

    def test_save_with_existing_thread_id(self, table: Table) -> None:
        """Test the save method with an existing thread."""
        thread_id = "01DXF6DT000000000000000000"
        table.put_item(
            Item={
                "thread_id": thread_id,
                "post_id": "-",
                "category": "Thread",
                "name": "Thread1",
                "created_at": Decimal("1577836800000000"),
            }
        )

        repository = DynamoDBThreadRepository(table)

        thread = Thread(id_=thread_id, name="Thread2", created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC))

        repository.save(thread)

        actual = table.get_item(Key={"thread_id": thread_id, "post_id": "-"})["Item"]
        expected = {
            "thread_id": thread_id,
            "post_id": "-",
            "category": "Thread",
            "name": "Thread2",
            "created_at": Decimal("1577840461000001"),
        }

        assert actual == expected

    def test_find_by_id_successful(self, table: Table) -> None:
        """Test the find_by_id method."""
        table.put_item(
            Item={
                "thread_id": "01DXF6DT000000000000000000",
                "post_id": "-",
                "category": "Thread",
                "name": "Thread1",
                "created_at": Decimal("1577840461000001"),
            }
        )

        repository = DynamoDBThreadRepository(table)

        thread_id = ULID.from_str("01DXF6DT000000000000000000")
        actual = repository.find_by_id(thread_id)

        expected = Thread(
            id_="01DXF6DT000000000000000000",
            name="Thread1",
            created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC),
        )

        assert actual == expected

    def test_find_by_id_with_nonexistent_thread(self, table: Table) -> None:
        """Test the find_by_id method with a nonexistent thread."""
        repository = DynamoDBThreadRepository(table)

        thread_id = ULID.from_str("01DXF6DT000000000000000000")
        actual = repository.find_by_id(thread_id)

        assert actual is None

    def test_list_all(self, table: Table) -> None:
        """Test the list_all method."""
        items = [
            {
                "thread_id": "01DXF6DT000000000000000000",
                "post_id": "-",
                "category": "Thread",
                "name": "Thread1",
                "created_at": Decimal("1577840461000001"),
            },
            {
                "thread_id": "01DXHRTH000000000000000000",
                "post_id": "-",
                "category": "Thread",
                "name": "Thread2",
                "created_at": Decimal("1577926861000001"),
            },
        ]
        for item in items:
            table.put_item(Item=item)  # type: ignore[arg-type]

        repository = DynamoDBThreadRepository(table)
        actual = repository.list_all()

        expected = [
            Thread(
                id_="01DXF6DT000000000000000000",
                name="Thread1",
                created_at=datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC),
            ),
            Thread(
                id_="01DXHRTH000000000000000000",
                name="Thread2",
                created_at=datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC),
            ),
        ]

        assert actual == expected

    def test_list_all_with_no_threads(self, table: Table) -> None:
        """Test the list_all method with no threads."""
        repository = DynamoDBThreadRepository(table)
        actual = repository.list_all()

        assert actual == []

    def test_delete_successful(self, table: Table) -> None:
        """Test the delete method."""
        thread_id = "01DXF6DT000000000000000000"
        table.put_item(
            Item={
                "thread_id": thread_id,
                "post_id": "-",
                "category": "Thread",
                "name": "Thread1",
                "created_at": Decimal("1577836800000000"),
            }
        )

        repository = DynamoDBThreadRepository(table)
        repository.delete(ULID.from_str(thread_id))

        actual = table.get_item(Key={"thread_id": thread_id, "post_id": "-"}).get("Item")
        assert actual is None

    def test_delete_with_nonexistent_thread(self, table: Table) -> None:
        """Test the delete method with a nonexistent thread."""
        repository = DynamoDBThreadRepository(table)
        with pytest.raises(ThreadNotFoundError, match="01DXF6DT000000000000000000"):
            repository.delete(ULID.from_str("01DXF6DT000000000000000000"))
