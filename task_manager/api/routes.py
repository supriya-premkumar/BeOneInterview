from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status

from task_manager.api.schemas import ErrorResponse, TaskRead, TaskWrite
from task_manager.service import TaskService
from task_manager.store import TaskNotFoundError

TASK_NOT_FOUND_RESPONSE = {
    "model": ErrorResponse,
    "description": "The task ID does not exist.",
}

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


def get_task_service() -> TaskService:
    raise RuntimeError("task service dependency was not configured")


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    description="Create a new task in the in-memory task store.",
)
def create_task(
    payload: TaskWrite,
    service: TaskService = Depends(get_task_service),
) -> TaskRead:
    task = service.create_task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
    )
    return TaskRead.model_validate(task)


@router.get(
    "",
    response_model=list[TaskRead],
    summary="List tasks",
    description="Return all tasks in insertion order.",
)
def list_tasks(service: TaskService = Depends(get_task_service)) -> list[TaskRead]:
    return [TaskRead.model_validate(task) for task in service.list_tasks()]


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="Get a task",
    description="Fetch a single task by its identifier.",
    responses={status.HTTP_404_NOT_FOUND: TASK_NOT_FOUND_RESPONSE},
)
def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> TaskRead:
    try:
        task = service.get_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found",
        ) from exc
    return TaskRead.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskRead,
    summary="Replace a task",
    description="Replace the title, description, and status for an existing task.",
    responses={status.HTTP_404_NOT_FOUND: TASK_NOT_FOUND_RESPONSE},
)
def replace_task(
    task_id: str,
    payload: TaskWrite,
    service: TaskService = Depends(get_task_service),
) -> TaskRead:
    try:
        task = service.replace_task(
            task_id=task_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
        )
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found",
        ) from exc
    return TaskRead.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task by its identifier.",
    responses={status.HTTP_404_NOT_FOUND: TASK_NOT_FOUND_RESPONSE},
)
def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> Response:
    try:
        service.delete_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found",
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
