"""Configuration for chat infrastructure unit tests."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import boto3
import pytest
from moto import mock_aws

if TYPE_CHECKING:
    from collections.abc import Iterator

    from mypy_boto3_dynamodb.client import DynamoDBClient
    from mypy_boto3_dynamodb.service_resource import Table


@pytest.fixture()
def _aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-northeast-1"


@pytest.fixture()
def aws(_aws_credentials: None) -> Iterator[DynamoDBClient]:
    """Fixture for the AWS DynamoDB client."""
    with mock_aws():
        yield boto3.client("dynamodb")


@pytest.fixture()
def _create_table(aws: Iterator[DynamoDBClient]) -> None:  # noqa: ARG001
    """Create the table in DynamoDB."""
    boto3.client("dynamodb").create_table(
        AttributeDefinitions=[
            {"AttributeName": "thread_id", "AttributeType": "S"},
            {"AttributeName": "post_id", "AttributeType": "S"},
            {"AttributeName": "category", "AttributeType": "S"},
        ],
        TableName=os.environ["TABLE_NAME"],
        KeySchema=[
            {"AttributeName": "thread_id", "KeyType": "HASH"},
            {"AttributeName": "post_id", "KeyType": "RANGE"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "by_category",
                "KeySchema": [
                    {"AttributeName": "category", "KeyType": "HASH"},
                    {"AttributeName": "thread_id", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )


@pytest.fixture()
def table(aws: Iterator[DynamoDBClient], _create_table: None) -> Table:  # noqa: ARG001
    """Fixture for the DynamoDB table."""
    return boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
