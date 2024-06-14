"""API stack."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_python_alpha as python

if TYPE_CHECKING:
    from aws_cdk.aws_dynamodb import Table
    from constructs import Construct


class Resource(TypedDict):
    """API resource."""

    methods: list[str]
    resources: dict[str, Resource]


class APIStack(Stack):
    """API stack."""

    lambda_: python.PythonFunction
    apigateway: apigateway.RestApi

    def __init__(self, scope: Construct, construct_id: str, table: Table) -> None:
        """Initialize the API stack."""
        super().__init__(scope, construct_id)

        lambda_function = self.create_lambda("Chat", table)
        self.create_api_gateway(lambda_function)

    def create_lambda(self, service_name: str, table: Table) -> python.PythonFunction:
        """Create the Lambda function.

        Args:
            service_name: The name of the service.
            table: The DynamoDB table.
        """
        src_dir = Path(__file__).parent.parent.parent / "src"
        self.lambda_ = python.PythonFunction(
            self,
            "Lambda",
            entry=src_dir.as_posix(),
            runtime=lambda_.Runtime.PYTHON_3_12,
            environment={"TABLE_NAME": table.table_name, "SERVICE_NAME": service_name},
        )
        table.grant_read_write_data(self.lambda_)

        return self.lambda_

    def _add_resources(self, target: apigateway.Resource, resources: Resource) -> None:
        for method in resources["methods"]:
            target.add_method(method)

        for name, resource in resources["resources"].items():
            child = target.add_resource(name)
            self._add_resources(child, resource)

    def create_api_gateway(self, lambda_function: python.PythonFunction) -> apigateway.RestApi:
        """Create the API Gateway.

        Args:
            lambda_function: The Lambda function for handler.
        """
        self.apigateway = apigateway.LambdaRestApi(self, "API", handler=lambda_function)

        resources: Resource = {"methods": [], "resources": {"threads": {"methods": ["POST", "GET"], "resources": {}}}}
        self._add_resources(self.apigateway.root, resources)

        return self.apigateway
