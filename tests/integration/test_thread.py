"""Integration tests for the thread router."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext
    from mypy_boto3_dynamodb.service_resource import Table

from src import index


class TestThread:
    """Test the thread router."""

    @pytest.mark.usefixtures("_create_table")
    def test_post_thread(self, context: LambdaContext) -> None:
        """Test POST /threads handler."""
        event = {
            "path": "/threads",
            "httpMethod": "POST",
            "requestContext": {"requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"},
            "body": '{"name": "Thread1"}',
        }

        actual = index.handler(event, context)

        body = json.loads(actual["body"])

        assert actual["statusCode"] == HTTPStatus.CREATED.value
        assert "id" in body
        assert body["name"] == "Thread1"
        assert "created_at" in body

    @pytest.mark.usefixtures("_create_table")
    def test_post_thread_invalid(self, context: LambdaContext) -> None:
        """Test POST /threads handler with invalid input."""
        event = {
            "path": "/threads",
            "httpMethod": "POST",
            "requestContext": {"requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"},
            "body": '{"name": ""}',
        }

        actual = index.handler(event, context)

        assert actual["statusCode"] == HTTPStatus.BAD_REQUEST.value
        assert "message" in actual["body"]

    @pytest.mark.usefixtures("_create_table")
    def test_get_threads(self, context: LambdaContext, table: Table) -> None:
        """Test GET /threads handler."""
        threads = [
            {
                "thread_id": "01DXF6DT000000000000000000",
                "post_id": "-",
                "category": "Thread",
                "name": "Thread1",
                "created_at": int(datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC).timestamp() * 1000000),
            },
            {
                "thread_id": "01DXHRTH000000000000000000",
                "post_id": "-",
                "category": "Thread",
                "name": "Thread2",
                "created_at": int(datetime(2020, 1, 2, 1, 1, 1, 1, tzinfo=UTC).timestamp() * 1000000),
            },
        ]
        for thread in threads:
            table.put_item(Item=thread)

        event = {
            "path": "/threads",
            "httpMethod": "GET",
            "requestContext": {"requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"},
        }

        actual = index.handler(event, context)

        body = json.loads(actual["body"])

        assert actual["statusCode"] == HTTPStatus.OK.value
        assert body["threads"] == [
            {
                "id": "01DXF6DT000000000000000000",
                "name": "Thread1",
                "created_at": "2020-01-01T01:01:01.000001Z",
            },
            {
                "id": "01DXHRTH000000000000000000",
                "name": "Thread2",
                "created_at": "2020-01-02T01:01:01.000001Z",
            },
        ]

    @pytest.mark.usefixtures("_create_table")
    def test_get_threads_empty(self, context: LambdaContext) -> None:
        """Test GET /threads handler with no threads."""
        event = {
            "path": "/threads",
            "httpMethod": "GET",
            "requestContext": {"requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"},
        }

        actual = index.handler(event, context)

        body = json.loads(actual["body"])

        assert actual["statusCode"] == HTTPStatus.OK.value
        assert body["threads"] == []
