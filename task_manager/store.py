from __future__ import annotations

from uuid import uuid4

from task_manager.models import Task, TaskStatus


class TaskNotFoundError(KeyError):
    """Raised when a task ID is not present in the store."""


class InMemoryTaskStore:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def add_task(
        self,
        title: str,
        description: str,
        status: TaskStatus = "pending",
    ) -> Task:
        task = Task(
            id=uuid4().hex,
            title=title,
            description=description,
            status=status,
        )
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Task:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def list_tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def update_task(
        self,
        task_id: str,
        title: str,
        description: str,
        status: TaskStatus,
    ) -> Task:
        self.get_task(task_id)
        updated_task = Task(
            id=task_id,
            title=title,
            description=description,
            status=status,
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: str) -> None:
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]
