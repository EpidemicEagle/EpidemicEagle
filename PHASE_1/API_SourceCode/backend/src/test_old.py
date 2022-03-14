from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


# global constants

a = "2018-xx-xx xx:xx:xx"
b = "2018-11-01 xx:xx:xx"
c = "2018-11-xx 17:00:xx"

# def test_covid():
#     response = client.get("/covid", params={"abc":"abc"})
#     assert response.status_code == 200
#     # assert response.json() == {"msg": "Hello World"}


def test_search():
    response = client.get("/api/search", params={"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2018-xx-xx xx:xx:xx", "key_terms":"wow,no", "location":"somewhere"})
    # assert response.status_code == 200
    # print(response.json())
    # assert response.json() == {"num_pages":1}