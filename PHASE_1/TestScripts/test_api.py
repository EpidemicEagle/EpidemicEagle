from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


# global constants

a = "2018-xx-xx xx:xx:xx"
b = "2018-11-01 xx:xx:xx"
c = "2018-11-xx 17:00:xx"


# /api/articles
# /api/articles/{article_id}
# /api/reports
# /api/reports/{report_id}
# /api/search

def test_search():
    params = {"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2018-xx-xx xx:xx:xx", "key_terms":"wow,no", "location":"somewhere"}
    response = client.get("/api/search", params=params)
    assert response.status_code == 200
    # assert keys exist in the response
    assert {'page_number', 'num_pages', 'results'} == set(response.json().keys())
