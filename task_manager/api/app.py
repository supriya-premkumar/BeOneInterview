from __future__ import annotations

from fastapi import FastAPI

from task_manager.api.routes import get_task_service, router
from task_manager.service import TaskService
from task_manager.store import InMemoryTaskStore


def create_app(service: TaskService | None = None) -> FastAPI:
    app = FastAPI(
        title="Task Manager API",
        version="1.0.0",
        summary="REST API for managing interview demo tasks.",
        description=(
            "A small, transport-isolated REST API for creating, reading, "
            "updating, and deleting tasks from an in-memory store."
        ),
        openapi_tags=[
            {
                "name": "tasks",
                "description": "Operations for managing task resources.",
            }
        ],
    )

    task_service = service or TaskService(InMemoryTaskStore())
    app.dependency_overrides[get_task_service] = lambda: task_service
    app.include_router(router)
    return app
