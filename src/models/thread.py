"""Models for threads."""

from __future__ import annotations

from datetime import datetime  # noqa: TCH003
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from chat.use_case import ThreadDTO


class NewThreadRequest(BaseModel):
    """Request model for creating a new thread."""

    name: str


class ThreadResponse(BaseModel):
    """Response model for a thread."""

    id_: str = Field(alias="id")
    name: str
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: ThreadDTO) -> Self:
        """Converts a DTO to a response model."""
        return cls(id=str(dto.id_), name=dto.name, created_at=dto.created_at)
