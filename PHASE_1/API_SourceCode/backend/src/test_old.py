from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


# global constants

a = "2018-xx-xx xx:xx:xx"
b = "2018-11-01 xx:xx:xx"
c = "2018-11-xx 17:00:xx"

# def test_article():
#     response = client.get("/api/articles/1")
#     print(response.json())
#     assert response.status_code == 200
#     print(response.json())
#     assert response.json()[0] == {}

def test_search():
    params = {"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2018-xx-xx xx:xx:xx", "key_terms":"wow,no", "location":"somewhere"}
    response = client.get("/api/search", params={"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2018-xx-xx xx:xx:xx", "key_terms":"wow,no", 'location':'sydney'})
    assert response.status_code == 200
    # assert keys exist in the response
    assert {'page_number', 'num_pages', 'results'} == set(response.json().keys())


def test_wrong_args():
    arg_test("/api/search")

def arg_test(url):
    params={"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2019-xx-xx xx:xx:xx", "key_terms":"covid, measles", "location":"Shanghai"}

    response = client.get(url, params =  {"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2019-xx-xx xx:xx:xx", "key_terms":"covid, measles"})
    assert response.status_code == 422

    response = client.get(url, params =  {"start_date":"2018-xx-xx xx:xx:xx", "end_date":"2019-xx-xx xx:xx:xx",  "location":"Shanghai"})
    assert response.status_code == 422

    response = client.get(url, params =  {"end_date":"2019-xx-xx xx:xx:xx", "key_terms":"covid, measles", "location":"Shanghai"})
    assert response.status_code == 422

    response = client.get(url, params =  {"start_date":"2018-xx-xx xx:xx:xx", "key_terms":"covid, measles", "location":"Shanghai"})
    assert response.status_code == 422

    response = client.get(url, params = {**params, 'start_date': 'two days from now'})
    assert response.status_code == 422

    response = client.get(url, params = {**params, 'end_date': 'today'})
    assert response.status_code == 422

    response = client.get(url, params = {**params, 'start_date': '2019-20-20'})
    assert response.status_code == 422

    response = client.get(url, params = {**params, 'end_date': '2019-20-20'})
    assert response.status_code == 422
