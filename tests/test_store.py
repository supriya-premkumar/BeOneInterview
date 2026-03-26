import pytest

from task_manager.models import Task
from task_manager.store import InMemoryTaskStore, TaskNotFoundError


def test_add_and_get_task() -> None:
    store = InMemoryTaskStore()

    created = store.add_task(
        title="Prepare interview demo",
        description="Build the first CRUD slice",
    )

    fetched = store.get_task(created.id)

    assert fetched == created
    assert fetched.status == "pending"


def test_list_tasks_returns_all_tasks_in_insert_order() -> None:
    store = InMemoryTaskStore()

    first = store.add_task("Task 1", "First task")
    second = store.add_task("Task 2", "Second task", status="started")

    assert store.list_tasks() == [first, second]


def test_update_task_replaces_mutable_fields() -> None:
    store = InMemoryTaskStore()
    created = store.add_task("Old title", "Old description")

    updated = store.update_task(
        task_id=created.id,
        title="New title",
        description="New description",
        status="complete",
    )

    assert updated == Task(
        id=created.id,
        title="New title",
        description="New description",
        status="complete",
    )
    assert store.get_task(created.id) == updated


def test_delete_task_removes_task() -> None:
    store = InMemoryTaskStore()
    created = store.add_task("Task to delete", "Temporary")

    store.delete_task(created.id)

    with pytest.raises(TaskNotFoundError):
        store.get_task(created.id)


def test_missing_task_operations_raise() -> None:
    store = InMemoryTaskStore()

    with pytest.raises(TaskNotFoundError):
        store.get_task("missing")

    with pytest.raises(TaskNotFoundError):
        store.update_task("missing", "Title", "Description", "pending")

    with pytest.raises(TaskNotFoundError):
        store.delete_task("missing")


def test_invalid_status_is_rejected() -> None:
    store = InMemoryTaskStore()

    with pytest.raises(ValueError):
        store.add_task("Task", "Description", status="done")  # type: ignore[arg-type]


def test_empty_title_is_rejected() -> None:
    store = InMemoryTaskStore()

    with pytest.raises(ValueError):
        store.add_task("   ", "Description")
