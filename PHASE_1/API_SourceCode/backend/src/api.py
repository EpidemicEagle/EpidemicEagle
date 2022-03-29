from fastapi import FastAPI, HTTPException, Query, Path, Depends, Request, Body
from fastapi.openapi.utils import get_openapi
from typing import List,Optional, Union
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
app = FastAPI(openapi_url="/api/v1/openapi.json")
# add stylesheet
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# Global Constants for regex
date_exact = r"^(\d{4})-(\d\d|xx)-(\d\d|xx) (\d\d|xx):(\d\d|xx):(\d\d|xx)$"
date_range = r"^(\d{4})-(\d\d|xx)-(\d\d|xx) (\ d\d|xx):(\d\d|xx):(\d\d|xx) to (\d{4})-(\d\d|xx)-(\d\d|xx) (\d\d|xx):(\d\d|xx):(\d\d|xx)$"

# Query Parameter Models

class SearchTerms(BaseModel):
    key_terms: str
    location: str
    start_date: str = Query(..., regex=date_exact)
    end_date: str = Query(..., regex=date_exact)
    page_number: Optional[int] = None   
    class Config:
        orm_mode = True

# Singular Models

class Location(BaseModel):
    country: str
    location: str
    class Config:
        orm_mode = True

class SearchResult(BaseModel):
    article_id: int
    url: str
    date_of_publication: str
    headline: str
    class Config:
        orm_mode = True

class Report(BaseModel):
    diseases: List[str]
    syndromes: List[str]
    event_date: str = Query(..., regex=date_range)
    locations: List[Location]
    class Config:
        orm_mode = True

class Article(BaseModel):
    url: str
    date_of_publication: str
    headline: str
    main_text: str
    reports: List[Report]
    class Config:
        orm_mode = True

# Pagination Models

class Pagination(BaseModel):
    num_pages: int
    page_number: int
    class Config:
        orm_mode = True

class ListSearchResult(Pagination):
    results: List[SearchResult]

class ListArticle(Pagination):
    articles: List[Article]

class ListReport(Pagination):
    reports: List[Report]

class foo(BaseModel):
    id : int



responses = {
    404: {"description": "Item not found"}
}

# TEST FUNCTIONS

# returns html
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

# # returns data from url api
# class Example(BaseModel):
#     name: int 
# @app.get("/", response_model=Example)
# async def example(item : int):
#     return Example(name=item)
# # optional parameter checked
# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: int = Path(..., title="The ID of the item to get"),
#     q: Optional[str] = Query(None, alias="item-query"),
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

# REAL FUNCTIONS


@app.get("/api/articles", response_model=ListArticle, tags=["api"])
def list_all_articles_with_params(
    key_terms: str,
    location: str,
    start_date: str = Query(..., regex=date_exact),
    end_date: str = Query(..., regex=date_exact),
    page_number: Optional[int] = None  
):
    """
    Lists all the articles specified within the parameters: start_date to end_date, key_terms and location.
    page_number can be specified to go to the corresponding page.
    """

    # query to get num results
    # num_pages = result_num_results

    # if page_number != 1:
    # query = """
    # ...
    # OFFSET 10*(page_number - 1)
    # LIMIT 10
    # """
    # else:
    # query = """
    # SELECT 
    # """

    # conn = c.cursor()

    # results = conn.exec(query)

    # if len(results) == 0:
    # return {
    #   "articles": [],
    #   "num_pages": 1,
    #   "page_number": 1
    # }


    #   articles = []
    # for line in query:
    #   articles.append(Article(url=line[0],date_of_publication=line[1],....))

    #    return {
    #     "articles": [],
    #     "num_pages": 1,
    #     "page_number": 1
    # }


    return {
        "articles": [],
        "num_pages": 1,
        "page_number": 1
    }

@app.get("/api/articles/{article_id}", response_model=Article, tags=["api"], responses={**responses})
def finds_article_by_id(article_id : int):
    """
    Lists all the information about an article from given id.
    """
    if article_id > 1000:
       raise HTTPException(status_code=404, detail="Article not found")

    return {}

@app.get("/api/reports", response_model=ListReport, tags=["api"])
def list_reports(
    key_terms: str,
    location: str,
    start_date: str = Query(..., regex=date_exact),
    end_date: str = Query(..., regex=date_exact),
    page_number: Optional[int] = None  
):
    """
    Lists all the reports specified within the parameters: start_date to end_date, key_terms and location.
    page_number can be specified to go to the corresponding page.
    """
    #    if item_id not in items:
    #    raise HTTPException(status_code=404, detail="Item not found")
    print(model)


    return {
        "reports": [],
        "num_pages": 1,
        "page_number": 1

    }

@app.get("/api/reports/{report_id}", response_model=Report, tags=["api"], responses={**responses})
def finds_report_by_id(report_id : int):
    """
    Lists all the information about a report from given id.
    """
    if report_id > 1000:
       raise HTTPException(status_code=404, detail="Report not found")

    return {}


@app.get("/api/search", response_model=ListSearchResult, tags=["api"])
def list_reports(
    key_terms: str,
    location: str,
    start_date: str = Query(..., regex=date_exact),
    end_date: str = Query(..., regex=date_exact),
    page_number: Optional[int] = None  
):
    """
    Lists all the search results specified within the parameters: start_date to end_date, key_terms and location.
    page_number can be specified to go to the corresponding page.
    """
    # check input is valid

    # HARD-CODED RESPONSE

    if "covid" in key_terms.lower() and "sydney" in location.lower():
        return {
            "results": [SearchResult(article_id=1, url="www.promed.com/mail",date_of_publication="2018-12-02", headline="Covid Strikes Sydney")],
            "num_pages": 1,
            "page_number": 1
        }           



    # TODO: GET id, url, date, heading from articles
    # WHERE word in keywords
    # AND location=location
    # OFFSET 10*page_number
    return {
        "results": [],
        "num_pages": 1,
        "page_number": 1
    } 


def custom_openapi():
    """Boilerplate to return swagger on /doc and prettySwagger on /redoc
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="EpidemicEagle API",
        version="v1",
        description="""
        This is an API to get news articles, reports and search results for diseases.
        Sample dates:
        - 2018-xx-xx xx:xx:xx
        - 2018-11-01 xx:xx:xx
        - 2018-11-xx 17:00:xx
        """,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
