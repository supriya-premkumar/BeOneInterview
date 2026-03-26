from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from task_manager.models import TaskStatus

NonEmptyTitle = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class TaskWrite(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Prepare interview demo",
                "description": "Expose CRUD operations over HTTP",
                "status": "pending",
            }
        }
    )

    title: NonEmptyTitle = Field(description="Short task title.")
    description: str = Field(description="Detailed task description.")
    status: TaskStatus = Field(
        default="pending",
        description="Task state. Allowed values: pending, started, complete.",
    )


class TaskRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "c9f8e27a9e664d98ad59cecfaf2d1f52",
                "title": "Prepare interview demo",
                "description": "Expose CRUD operations over HTTP",
                "status": "pending",
            }
        },
    )

    id: str = Field(description="Unique task identifier.")
    title: str = Field(description="Short task title.")
    description: str = Field(description="Detailed task description.")
    status: TaskStatus = Field(description="Current task state.")


class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"detail": "task not found"}}
    )

    detail: str = Field(description="Human-readable error message.")
