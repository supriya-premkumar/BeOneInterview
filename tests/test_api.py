from __future__ import annotations

from fastapi.testclient import TestClient

from task_manager.api import create_app
from task_manager.service import TaskService
from task_manager.store import InMemoryTaskStore


def make_client() -> TestClient:
    service = TaskService(InMemoryTaskStore())
    app = create_app(service=service)
    return TestClient(app)


def test_create_and_get_task_via_api() -> None:
    client = make_client()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Prepare interview demo",
            "description": "Expose CRUD over HTTP",
            "status": "pending",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()

    get_response = client.get(f"/tasks/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.json() == created


def test_list_tasks_via_api() -> None:
    client = make_client()

    first = client.post(
        "/tasks",
        json={"title": "Task 1", "description": "First", "status": "pending"},
    ).json()
    second = client.post(
        "/tasks",
        json={"title": "Task 2", "description": "Second", "status": "started"},
    ).json()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [first, second]


def test_put_replaces_task_via_api() -> None:
    client = make_client()
    created = client.post(
        "/tasks",
        json={"title": "Old", "description": "Old desc", "status": "pending"},
    ).json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={
            "title": "New",
            "description": "New desc",
            "status": "complete",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": created["id"],
        "title": "New",
        "description": "New desc",
        "status": "complete",
    }


def test_delete_task_via_api() -> None:
    client = make_client()
    created = client.post(
        "/tasks",
        json={"title": "Delete me", "description": "Soon gone", "status": "pending"},
    ).json()

    delete_response = client.delete(f"/tasks/{created['id']}")
    get_response = client.get(f"/tasks/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "task not found"}


def test_missing_task_returns_404() -> None:
    client = make_client()

    response = client.get("/tasks/missing")

    assert response.status_code == 404
    assert response.json() == {"detail": "task not found"}


def test_invalid_payload_returns_422() -> None:
    client = make_client()

    response = client.post(
        "/tasks",
        json={"title": "", "description": "Invalid", "status": "done"},
    )

    assert response.status_code == 422


def test_openapi_spec_exposes_task_contract() -> None:
    client = make_client()

    response = client.get("/openapi.json")

    assert response.status_code == 200
    spec = response.json()
    assert spec["info"]["title"] == "Task Manager API"
    assert spec["info"]["version"] == "1.0.0"
    assert "/tasks" in spec["paths"]
    assert "/tasks/{task_id}" in spec["paths"]
    assert spec["paths"]["/tasks"]["post"]["summary"] == "Create a task"
    assert spec["paths"]["/tasks/{task_id}"]["put"]["summary"] == "Replace a task"
