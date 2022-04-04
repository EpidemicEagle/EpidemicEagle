from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query, Path, Depends, Request, Body, Form
from fastapi.openapi.utils import get_openapi
from typing import List,Optional, Union
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import json
app = FastAPI(openapi_url="/api/v1/openapi.json")
# add stylesheet
app.mount("/css", StaticFiles(directory="templates/css"), name="css")
app.mount("/js", StaticFiles(directory="templates/js"), name="js")
app.mount("/images", StaticFiles(directory="templates/images"), name="images")
app.mount("/webfonts", StaticFiles(directory="templates/webfonts"), name="webfonts")


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

################################
#
# FAKE FUNCTIONS
#
################################

@app.get("/form")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/form")
def form_post(request: Request, num: int = Form(...)):
    return templates.TemplateResponse('form.html', context={'request': request, 'result': num})


@app.get("/dummy", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("dummy.html", {"request": request})

################################
#
# REAL FUNCTIONS
#
################################

def parse_report_info(keyword, article):
    return set([_ for _ in [_[keyword] for _ in article['reports']] for _ in _])

# unify index calls
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/index.html", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# QUICK SEARCH
# qsearch search box
@app.get("/qsearch", response_class=HTMLResponse)
async def q(request: Request):
    return templates.TemplateResponse("qsearch.html", {"request": request})

# qsearch table
@app.post("/qsearch", response_class=HTMLResponse)
async def q(request: Request,
    location: Optional[str] = Form(...),
):
    f = open('sample_file.json')
    data= json.load(f)['articles']
    f.close()
    searches = []
    count = 0
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now()

    # average time is 3000 ms (3 seconds)
    for article in data:
        if count == 10:
            break
        # exclude and pagination
        date = datetime.strptime(article['dateOfPublication'], '%d %B %Y')

        if start_date < date and date < end_date:
            locations = parse_report_info('locations', article)
            if location in locations:
                searches.append(article)
                count += 1
        count += 1
    
        
    print(searches)

    return templates.TemplateResponse("qsearch.html", 
    {
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        "request": request,
        "searches": searches,
    }
    )

# REPORT SEARCH
# reports get
@app.get("/reports", response_class=HTMLResponse)
async def reports(request: Request):
    return templates.TemplateResponse("reports_get.html", {"request": request})

# reports post
@app.post("/reports", response_class=HTMLResponse)
async def reports_post(request: Request,
    key_terms: str,
    location: str,
    start_date: str = Query(..., regex=date_exact),
    end_date: str = Query(..., regex=date_exact),
    page_number: Optional[int] = None  
):

    f = open('reports.json')
    data = json.load(f)['reports']
    f.close()
    reports = []
    count = 0
    locations = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua & Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia & Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central Arfrican Republic","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cuba","Curacao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Namibia","Nauro","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","North Korea","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre & Miquelon","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","St Kitts & Nevis","St Lucia","St Vincent","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad & Tobago","Tunisia","Turkey","Turkmenistan","Turks & Caicos","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States of America","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"];
    
    for report in data:
        if count >= 10:
            break
        # check date of report
        date = datetime.strptime(report['eventDate'], '%d %B %Y')
        if start_date < date and date < end_date:
            #check each location of report
            for replocation in report['locations']:
                # check report location is valid and is searched location
                if replocation in locations and replocation = location:
                    # check key terms
                    if key_terms in report['diseases']:
                        reports.append(report)
                        count += 1
                    # can stop checking report locations
                    break

    return templates.TemplateResponse("reports_post.html", 
    {
        "key_terms": key_terms,
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        "page_number": page_number,
        "request": request,
        "reports": reports,
    }
    )


# COMPLETE SEARCH
# search get
@app.get("/completesearch", response_class=HTMLResponse)
async def search(request: Request):
    return templates.TemplateResponse("dummy.html", {"request": request})

# search post
@app.post("/completesearch", response_class=HTMLResponse)
async def search_post(request: Request,
    key_terms: str = Form(...),
    disease: str = Form(...),
    location: str = Form(...),
    start_date: datetime  = Form(...),
    end_date: datetime = Form(...),
    page_number: Optional[int] = None  
):
    # test dates
    # test location


    f = open('sample_file.json')
    data= json.load(f)['articles']
    f.close()
    searches = []
    count = 0

    # average time is 3000 ms (3 seconds)
    for article in data:
        if count == 10:
            break
        # exclude and pagination
        date = datetime.strptime(article['dateOfPublication'], '%d %B %Y')

        # do easy comparision before hard comparision
        if start_date < date and date < end_date:
            # then limit by the harder values
            diseases = parse_report_info('diseases', article)
            locations = parse_report_info('locations', article)
            if disease in diseases and location in locations:
                # change response to fit html better
                article.update(dateOfPublication=date)
                searches.append(article)
                count += 1
        
    # print(searches)

    return templates.TemplateResponse("quicksearch.html", 
    {
        "key_terms": key_terms,
        "disease": disease,
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        "page_number": page_number,
        "request": request,
        "searches": searches
    }
    )

# articles get 
@app.get("/articles", response_class=HTMLResponse)
async def articles(request: Request):
    return templates.TemplateResponse("articles_get.html", {"request": request})




# articles id get
@app.get("/articles/{id}", response_class=HTMLResponse)
async def id_articles(request: Request, id: str):
    f = open("articles.json")
    data = json.load(f)['articles']
    length = len(data)

    # return 'no articles found if greater than num of articles"
    if int(id) > length or int(id) < 0:
        return templates.TemplateResponse("entry_article.html", {"request": request, "id": id})
        
    report = data[int(id)]    
    # TODO: 
    # pip freeze > requirements.txt
    # get the ['url'] form the data
    # scrape the url
    #   installing selenium in project foler
    # pull relevant data (body of text)
    # integrate it into entry_article.html
    # match index.html style if time permits
    # (use styles.css (font-size if necessary))

    return templates.TemplateResponse("entry_article.html", {"request": request, "id": id, 'article' : report})

## API functions

@app.get("/api/v1/articles", response_model=ListArticle, tags=["api"])
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
    return {
        "articles": [],
        "num_pages": 1,
        "page_number": 1
    }

@app.get("/api/v1/articles/{article_id}", response_model=Article, tags=["api"], responses={**responses})
def finds_article_by_id(article_id : int):
    """
    Lists all the information about an article from given id.
    """
    if article_id > 1000:
       raise HTTPException(status_code=404, detail="Article not found")

    return Article(
        url="sample_url",
        date_of_publication="2018-xx-xx xx:xx:xx",
        headline="sample headline",
        main_text="sample text",
        reports=[Report(diseases=[],
                        syndromes=[],
                        event_date="2018-xx-xx xx:xx:xx to 2018-xx-xx xx:xx:xx",
                        locations=[]
                )]
        )

@app.get("/api/v1/reports", response_model=ListReport, tags=["api"])
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
    # print(model)


    return {
        "reports": [],
        "num_pages": 1,
        "page_number": 1

    }

@app.get("/api/v1/reports/{report_id}", response_model=Report, tags=["api"], responses={**responses})
def finds_report_by_id(report_id : int):
    """
    Lists all the information about a report from given id.
    """
    if report_id > 1000:
       raise HTTPException(status_code=404, detail="Report not found")

    # report format has to be sent
    return Report(diseases=[],
                    syndromes=[],
                    event_date="2018-xx-xx xx:xx:xx to 2018-xx-xx xx:xx:xx",
                    locations=[]
                )

@app.get("/api/v1/search", response_model=ListSearchResult, tags=["api"])
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
