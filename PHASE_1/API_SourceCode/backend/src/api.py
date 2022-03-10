from fastapi import FastAPI, HTTPException, Query, Path, Depends
from fastapi.openapi.utils import get_openapi
from typing import List,Optional, Union
from pydantic import BaseModel
import datetime
import requests
app = FastAPI(openapi_url="/api/v1/openapi.json")

# Global Constants for regex
date_exact = r"^(\d{4})-(\d\d|xx)-(\d\d|xx) (\d\d|xx):(\d\d|xx):(\d\d|xx)$"
date_range = r"^(\d{4})-(\d\d|xx)-(\d\d|xx) (\ d\d|xx):(\d\d|xx):(\d\d|xx) to (\d{4})-(\d\d|xx)-(\d\d|xx) (\d\d|xx):(\d\d|xx):(\d\d|xx)$"

# TODO: Don't return the class for json element
# E.G. Dont return Report(syndromes=""..)
# create your own json model, which is identical to the class


# Query Parameter Models

class SearchTerms(BaseModel):
    key_terms: str
    location: str
    start_date: str = Query(..., regex=date_exact)
    end_date: str = Query(..., regex=date_exact)
    page_number: Optional[int] = None   

# Singular Models

class Location(BaseModel):
    country: str
    location: str

class SearchResult(BaseModel):
    article_id: int
    url: str
    date_of_publication: str
    headline: str

class Report(BaseModel):
    diseases: List[str]
    syndromes: List[str]
    event_date: str = Query(..., regex=date_range)
    locations: List[Location]

class Article(BaseModel):
    url: str
    date_of_publication: str
    headline: str
    main_text: str
    reports: List[Report]

# Pagination Models

class Pagination(BaseModel):
    num_pages: str
    page_number: str

class ListSearchResult(Pagination):
    results: List[SearchResult]

class ListArticle(Pagination):
    articles: List[Article]

class ListReport(Pagination):
    reports: List[Report]

# to make class a dict, dic = object.dic()

# TEST FUNCTIONS
@app.get("/covid")
def covid_cases():
    return [{"cases": 192082}]

@app.post("/covid/{item_id}")
def covid_cases(item_id: int):
    
    r = requests.get("https://corona.lmao.ninja/v2/continents")
    return [{
        "cases": r.json()[0]['cases'],
        "id": item_id
        }]

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.get("/api/analyse")
async def read_item_for_analyse(
    start_date: str = Query(..., regex=r"[\d]{4}-[\d]{1,2}-[\d]{1,2}"),
    end_date: str = Query(..., regex=r"[\d]{4}-[\d]{1,2}-[\d]{1,2}", description="Test description"),
    increment: int = None,
):
    return [{"cases": 192082}]


# REAL FUNCTIONS


@app.get("/api/articles", response_model=ListArticle, tags=["api"])
def list_all_articles_with_params(model: SearchTerms = Depends()):
    """
    Lists all the articles specified within the parameters: start_date to end_date, key_terms and location.
    page_number can be specified to go to the corresponding page.
    """

    #    if item_id not in items:
    #    raise HTTPException(status_code=404, detail="Item not found")

    return [{
        "articles": [],
        "num_pages": 1,
        "page_number": 1

    }]

@app.get("/api/articles/{article_id}", response_model=Article, tags=["api"])
def finds_article_by_id(article_id):
    """
    Lists all the information about an article from given id.
    """
    #    if item_id not in items:
    #    raise HTTPException(status_code=404, detail="Item not found")

    return [{}]

@app.get("/api/reports", response_model=ListReport, tags=["api"])
def list_reports(model: SearchTerms = Depends()):
    """
    Lists all the reports specified within the parameters: start_date to end_date, key_terms and location.
    page_number can be specified to go to the corresponding page.
    """
    #    if item_id not in items:
    #    raise HTTPException(status_code=404, detail="Item not found")

    return [{
        "reports": [],
        "num_pages": 1,
        "page_number": 1

    }]

@app.get("/api/reports/{report_id}", response_model=Report, tags=["api"])
def finds_report_by_id(report_id):
    """
    Lists all the information about a report from given id.
    """
    #    if item_id not in items:
    #    raise HTTPException(status_code=404, detail="Item not found")

    return [{}]


@app.get("/api/search", tags=["api"])
def list_search_results(model: SearchTerms = Depends()):
    """
    Lists all the search results specified within the parameters: start_date to end_date, key_terms and location.
    page_number can be specified to go to the corresponding page.
    """
    # check input is valid

    # TODO: GET id, url, date, heading from articles
    # WHERE word in keywords
    # AND location=location
    # OFFSET 10*page_number
    return [{
        "results": [{"a":"c"}],
        "num_pages": 1,
        "page_number": 1
    }]   


def custom_openapi():
    """Boilerplate to return swagger on /doc and prettySwagger on /redoc
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="EpidemicEagle API",
        version="v1",
        description="This is an API to get news articles, reports and search results for diseases",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
