from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_invalid_extension():
    response = client.post(
        "/api/v1/documents/ingest",
        files={
            "file": (
                "test.jpg",
                b"fake image",
                "image/jpeg",
            )
        },
        data={
            "chunking_strategy": "fixed"
        },
    )

    assert response.status_code == 400