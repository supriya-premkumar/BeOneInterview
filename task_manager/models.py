from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal

TaskStatus = Literal["pending", "started", "complete"]

ALLOWED_STATUSES: Final[set[str]] = {"pending", "started", "complete"}


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if self.status not in ALLOWED_STATUSES:
            raise ValueError(f"status must be one of: {sorted(ALLOWED_STATUSES)}")
