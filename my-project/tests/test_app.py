from fastapi.testclient import TestClient

from app.main import app


def test_root_returns_same_html_page() -> None:
    client = TestClient(app)

    first_response = client.get("/")
    second_response = client.get("/")

    for response in (first_response, second_response):
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")
        assert "<title>Hola mundo</title>" in response.text
        assert "<h1>Hola mundo</h1>" in response.text

    assert first_response.content == second_response.content
