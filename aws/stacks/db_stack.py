"""CDK stack for the database resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aws_cdk import Stack
from aws_cdk import aws_dynamodb as dynamodb

if TYPE_CHECKING:
    from constructs import Construct


class DBStack(Stack):
    """Stack for the database resources."""

    table: dynamodb.TableV2

    def __init__(self, scope: Construct, construct_id: str) -> None:
        """Initialize the stack.

        Args:
            scope: The parent construct.
            construct_id: The construct ID.
            kwargs: Additional keyword arguments.
        """
        super().__init__(scope, construct_id)

        self.table = dynamodb.TableV2(
            self,
            "Table",
            partition_key=dynamodb.Attribute(name="thread_id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="post_id", type=dynamodb.AttributeType.STRING),
            global_secondary_indexes=[
                dynamodb.GlobalSecondaryIndexPropsV2(
                    index_name="by_category",
                    partition_key=dynamodb.Attribute(name="category", type=dynamodb.AttributeType.STRING),
                )
            ],
        )
