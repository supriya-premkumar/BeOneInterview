from __future__ import annotations

from task_manager.models import Task, TaskStatus
from task_manager.store import InMemoryTaskStore


class TaskService:
    """Transport-agnostic application layer for task operations."""

    def __init__(self, store: InMemoryTaskStore) -> None:
        self._store = store

    def create_task(
        self,
        title: str,
        description: str,
        status: TaskStatus = "pending",
    ) -> Task:
        return self._store.add_task(
            title=title,
            description=description,
            status=status,
        )

    def get_task(self, task_id: str) -> Task:
        return self._store.get_task(task_id)

    def list_tasks(self) -> list[Task]:
        return self._store.list_tasks()

    def replace_task(
        self,
        task_id: str,
        title: str,
        description: str,
        status: TaskStatus,
    ) -> Task:
        return self._store.update_task(
            task_id=task_id,
            title=title,
            description=description,
            status=status,
        )

    def delete_task(self, task_id: str) -> None:
        self._store.delete_task(task_id)
