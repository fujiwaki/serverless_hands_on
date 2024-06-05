"""Thread model."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict
from ulid import ULID


class Thread(BaseModel):
    """Thread model."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    id_: ULID
    name: str
    created_at: datetime

    @classmethod
    def new(cls, name: str) -> Thread:
        """Create new thread."""
        return cls(id_=ULID(), name=name, created_at=datetime.now(tz=UTC))
