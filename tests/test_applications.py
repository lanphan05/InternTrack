import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def empty_storage():
    """Start every test with no saved applications and ids counting from 1."""
    main.applications.clear()
    main.next_id = 1
    yield
    main.applications.clear()
    main.next_id = 1


def test_create_application_with_all_fields_returns_201_and_saved_record():
    payload = {
        "company": "IBM",
        "role": "Software Developer Intern",
        "link": "https://example.com/job",
        "status": "applied",
        "date_applied": "2026-11-26",
        "notes": "Applied through the careers page.",
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 201
    assert response.json() == {"id": 1, **payload}


def test_create_application_applies_defaults_for_optional_fields():
    response = client.post(
        "/applications", json={"company": "IBM", "role": "Developer Intern"}
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "company": "IBM",
        "role": "Developer Intern",
        "link": None,
        "status": "wishlist",
        "date_applied": None,
        "notes": "",
    }


def test_server_assigns_new_ids_and_ignores_client_id():
    first = client.post("/applications", json={"company": "IBM", "role": "Intern"})
    second = client.post(
        "/applications", json={"id": 99, "company": "Acme", "role": "Intern"}
    )

    assert first.json()["id"] == 1
    assert second.json()["id"] == 2


@pytest.mark.parametrize("field", ["company", "role"])
@pytest.mark.parametrize("blank_value", ["", "   "])
def test_blank_required_field_returns_422_and_saves_nothing(field, blank_value):
    payload = {"company": "IBM", "role": "Developer Intern", field: blank_value}

    response = client.post("/applications", json=payload)

    assert response.status_code == 422
    assert main.applications == {}


@pytest.mark.parametrize("field", ["company", "role"])
def test_missing_required_field_returns_422(field):
    payload = {"company": "IBM", "role": "Developer Intern"}
    del payload[field]

    response = client.post("/applications", json=payload)

    assert response.status_code == 422
    assert main.applications == {}


def test_unsupported_status_returns_422():
    response = client.post(
        "/applications",
        json={"company": "IBM", "role": "Intern", "status": "Applied"},
    )

    assert response.status_code == 422
    assert main.applications == {}


def test_list_applications_returns_empty_list_when_none_saved():
    response = client.get("/applications")

    assert response.status_code == 200
    assert response.json() == []


def test_list_applications_returns_every_saved_record():
    first = client.post("/applications", json={"company": "IBM", "role": "Intern"})
    second = client.post(
        "/applications",
        json={"company": "Acme", "role": "Backend Intern", "status": "applied"},
    )

    response = client.get("/applications")

    assert response.status_code == 200
    assert response.json() == [first.json(), second.json()]


def test_get_application_returns_record_created_earlier():
    payload = {
        "company": "IBM",
        "role": "Software Developer Intern",
        "link": "https://example.com/job",
        "status": "applied",
        "date_applied": "2026-11-26",
        "notes": "Applied through the careers page.",
    }
    created = client.post("/applications", json=payload).json()

    response = client.get(f"/applications/{created['id']}")

    assert response.status_code == 200
    assert response.json() == {"id": created["id"], **payload}


def test_get_application_with_unknown_id_returns_404():
    client.post("/applications", json={"company": "IBM", "role": "Intern"})

    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_get_application_with_non_integer_id_returns_422():
    response = client.get("/applications/abc")

    assert response.status_code == 422
