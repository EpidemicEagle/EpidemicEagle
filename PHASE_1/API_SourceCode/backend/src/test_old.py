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


def test_report():
    params = {"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2018-xx-xx xx:xx:xx", "key_terms":"wow,no", "location":"somewhere"}
    response = client.get("/api/reports", params=params)
    assert response.status_code == 200
    # assert keys exist in the response
    assert {'page_number', 'num_pages', 'reports'} == set(response.json().keys())

def test_report_id():
    id = 1
    response = client.get(f"/api/reports/{id}")
    assert response.status_code == 200

def test_report_id_too_big():
    id = 1200
    response = client.get(f"/api/reports/{id}")
    assert response.status_code == 404

def test_article():
    params = {"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2018-xx-xx xx:xx:xx", "key_terms":"wow,no", "location":"somewhere"}
    response = client.get("/api/articles", params=params)
    assert response.status_code == 200
    # assert keys exist in the response
    assert {'page_number', 'num_pages', 'articles'} == set(response.json().keys())

def test_article_id():
    id = 1
    response = client.get(f"/api/articles/{id}")
    assert response.status_code == 200

def test_article_id_too_big():
    id = 1200
    response = client.get(f"/api/articles/{id}")
    assert response.status_code == 404

def test_search():
    params = {"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2018-xx-xx xx:xx:xx", "key_terms":"wow,no", "location":"somewhere"}
    response = client.get("/api/search", params=params)
    assert response.status_code == 200
    # assert keys exist in the response
    assert {'page_number', 'num_pages', 'results'} == set(response.json().keys())