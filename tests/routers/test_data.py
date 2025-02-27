from fastapi.testclient import TestClient

from app.config import settings
from app.main import web_app

client = TestClient(web_app)


def test_create_translation() -> None:
    data = {
        "from_dialect": "mysql",
        "to_dialect": "postgres",
        "sql": "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d') AS FORMATTED_DATE;",
    }
    response = client.post(settings.API_V1_STR + "/translate", json=data)
    assert response.status_code == 200
    assert response.json() == "SELECT TO_CHAR(NOW(), 'YYYY-MM-DD') AS FORMATTED_DATE;"


def test_create_translation_returns_parse_error() -> None:
    data = {
        "from_dialect": "mysql",
        "to_dialect": "postgres",
        "sql": "SELECT foo FROM (SELECT baz FROM t",
    }
    response = client.post(settings.API_V1_STR + "/translate", json=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "ParseError",
            "message": "Expecting ). Line 1, Col: 34.\n  SELECT foo FROM (SELECT baz FROM \u001b[4mt\u001b[0m",
            "description": "Expecting )",
            "line": 1,
            "col": 34,
            "start_context": "SELECT foo FROM (SELECT baz FROM ",
            "highlight": "t",
            "end_context": "",
            "into_expression": None,
        }
    }


## TODO: add test for unsupported errors
