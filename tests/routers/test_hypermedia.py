from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
