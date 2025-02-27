from fastapi.testclient import TestClient

from app.main import web_app

client = TestClient(web_app)


def test_home() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
