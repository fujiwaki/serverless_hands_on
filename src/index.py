"""Lambda function entrypoint."""

import os
from typing import Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from chat.config.container import Container
from routers import thread

logger = Logger(service=os.environ["SERVICE_NAME"])

app = ApiGatewayResolver()
app.include_router(thread.router, prefix="/thread")

container = Container(os.environ["TABLE_NAME"])


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
def handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    """Lambda function handler."""
    app.append_context(container=container)
    return app.resolve(event, context)
