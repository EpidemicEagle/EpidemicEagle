from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_covid():
    response = client.get("/covid", params={"abc":"abc"})
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}