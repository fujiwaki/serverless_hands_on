"""Thread router module."""

from http import HTTPStatus
from typing import TYPE_CHECKING

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.event_handler.router import APIGatewayRouter
from chat.use_case import CreateThreadCommand
from models.thread import NewThreadRequest, ThreadResponse
from pydantic import ValidationError

if TYPE_CHECKING:
    from chat.config.container import Container


logger = Logger(child=True)
router = APIGatewayRouter()


@router.post("/")
def post_threads(request: NewThreadRequest) -> Response[ThreadResponse]:
    """POST /threads handler."""
    container: Container = router.context["container"]
    command = CreateThreadCommand(name=request.name)
    try:
        thread = container.create_thread.execute(command)
    except ValidationError as e:
        raise BadRequestError(str(e)) from e
    return Response(
        status_code=HTTPStatus.CREATED.value, body=ThreadResponse.from_dto(thread).model_dump_json(by_alias=True)
    )


@router.get("/")
def get_threads() -> dict[str, list[ThreadResponse]]:
    """GET /threads handler."""
    container: Container = router.context["container"]
    threads = container.list_threads.execute()
    return {"threads": [ThreadResponse.from_dto(thread) for thread in threads]}
