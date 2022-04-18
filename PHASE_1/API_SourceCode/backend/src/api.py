from datetime import datetime, timedelta
from resource import RLIMIT_CPU
from fastapi import FastAPI, HTTPException, Query, Request, Form
from fastapi.openapi.utils import get_openapi
from typing import List,Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from starlette.responses import PlainTextResponse, RedirectResponse
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

users = []

################################
#
# FAKE FUNCTIONS
#
################################

@app.get("/dummy", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("completesearch.html", {"request": request})

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

@app.get("/login", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


def send_user_login(request, user):
    # also sends
    # username 
    # current trip (SYD -> CHN)
    # container
    # Start Date   || Current Risk Level (API)
    # End   Date   || Vaccination Rate (API)
    # Send Message || Reports on Current Destination
    # (          ) ||
    #         (go) ||
    dest = user['destination']
    url = "https://disease.sh/v3/covid-19/countries/" + dest + "?strict=true"
    response = requests.get(url)
    data = response.json()
    return templates.TemplateResponse("traveller.html", {"request": request, "user": user, "covid_data" : data})

@app.post("/login", response_class=HTMLResponse)
async def index(request: Request,
    email: Optional[str] = Form(...),
    password: Optional[str] = Form(...),
    type: Optional[str] = Form(...),
    ):
    print(email, password, type)
    f = open('users.json', 'r+')
    data = json.load(f)
    print(data)
    users = data['travellers']
    if type == 'user':
        users = data['travellers']
        for user in users:
            if user['email'] == email and user['password'] == password:
                send_user_login(request, user)
        return templates.TemplateResponse("login.html", {"request": request, "wrong_user" : True})
    else:
        agencies = data['agencies']
        for agency in agencies:
            if agency['email'] == email and agency['password'] == password:
                return templates.TemplateResponse("agency.html", {"request": request, "user": user})
        return templates.TemplateResponse("login.html", {"request": request, "wrong_agency" : True})


@app.get("/agency", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("agency.html", {"request": request})

# QUICK SEARCH
# qsearch search box
@app.get("/qsearch", response_class=HTMLResponse)
async def q(request: Request):
    return templates.TemplateResponse("qsearch.html", {"request": request})

def risk_level(location):
    f = open("country_codes.json", 'r')
    data = json.load(f)
    code = data.get(location, "not found")
    if code == 'not found':
        return "No risk data detected."
    else:
        response = requests.get('https://www.travel-advisory.info/api')
        a = response.json()['data'][code]['advisory']
    return a


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
    
    rl = risk_level(location)
    print(rl)
    return templates.TemplateResponse("qsearch.html", 
    {
        "location": location,
        "request": request,
        "searches": searches,
        "risk_level": rl
    }
    )

# REPORT SEARCH
# reports get
@app.get("/reports", response_class=HTMLResponse)
async def reports(request: Request):
    return templates.TemplateResponse("reports.html", {"request": request})

# reports post
@app.post("/reports", response_class=HTMLResponse)
async def reports(request: Request,
    location: str = Form(...),
    start_date: datetime = Form(...),
    end_date: datetime = Form(...),
    # page_number: Optional[int] = None  
):

    f = open('reports_file_v2.json')
    data = json.load(f)['reports']
    f.close()
    reports = []
    count = 0
    locations = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua & Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia & Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central Arfrican Republic","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cuba","Curacao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Namibia","Nauro","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","North Korea","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre & Miquelon","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","St Kitts & Nevis","St Lucia","St Vincent","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad & Tobago","Tunisia","Turkey","Turkmenistan","Turks & Caicos","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States of America","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"];
    
    for report in data:
        if count >= 10:
            break
        # check date of report
        date = datetime.strptime(report['eventDate'], "%Y-%M-%d")
        if start_date < date and date < end_date:

            #check each location of report
            for replocation in report['locations']:
                # check report location is valid and is searched location
                if replocation in locations and replocation == location:
                    # check key terms
                    # if key_terms in report['diseases']:
                    report["l_diseases"] = ", ".join(report['diseases'])
                    report["l_locations"] = ", ".join(report['locations'])
                    # change the report for html
                    reports.append(report)
                    count += 1
                    # can stop checking report locations
                    break
    return templates.TemplateResponse("reports.html", 
    {
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        # "page_number": page_number,
        "request": request,
        "reports": reports,
    }
    )


# COMPLETE SEARCH
# search get
@app.get("/completesearch", response_class=HTMLResponse)
async def search(request: Request):
    return templates.TemplateResponse("completesearch.html", {"request": request})

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

    return templates.TemplateResponse("completesearch.html", 
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

# articles id get
@app.get("/articles/{id}", response_class=HTMLResponse)
async def id_articles(request: Request, id):
    # f = open("articles.json")
    # data = json.load(f)['articles']
    # length = len(data)

    # return 'no articles found if greater than num of articles"
    # if int(id) > length or int(id) < 0:
    #     return templates.TemplateResponse("entry_article.html", {"request": request, "id": id})
    # report = data[int(id)]    
    return templates.TemplateResponse("entry.html", {"request": request, "id": id})


# traveller get
@app.get("/traveller", response_class=HTMLResponse)
async def traveller(request: Request):
    return templates.TemplateResponse("traveller.html", {"request": request})


# traveller post
@app.post("/traveller", response_class=HTMLResponse)
async def traveller_dash(request: Request):
    found_user = None
    for user in users:
        if user["id"] == id:
            found_user = user
            break
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    # sample user
    found_user = {
        "name": "Treav",
        "start_loc": "Aus",
        "end_loc": "China",
        "start_date": start_date,
        "end_date": end_date,
        "reports": [],
    }
    if found_user: 
        return templates.TemplateResponse("traveller.html", 
        {
            "user": found_user,
            "request": request,
        }
        

    
        )
    else:
        # user not found, try again
        return templates.TemplateResponse("traveller.html", 
        {
            
            "request": request,
        }
        )



# traveller get
@app.get("/edit", response_class=HTMLResponse)
async def traveller_edit(request: Request):
    return templates.TemplateResponse("traveller_edit.html", {"request": request})


# traveller post
@app.post("/edit", response_class=HTMLResponse)
async def traveller_dash_edit(request: Request):
    found_user = None
    for user in users:
        if user["id"] == id:
            found_user = user
            break
    found_user = {
        "name": "testing",
    }
    if found_user: 
        """
            "traveller": request,
            "start_loc": start_loc,
            "end_loc": end_loc,
            "start_date": start_date,
            "end_date": end_date,
            "reports": reports,
        """
        return templates.TemplateResponse("traveller_edit.html", 
        {
            
            "user": found_user,
            "request": request,
            
        }
        

    
        )
    else:
        # user not found, try again
        return templates.TemplateResponse("traveller_edit.html", 
        {
            
            "request": request,
        }
        )

# travel agency get
@app.get("/travelagency", response_class=HTMLResponse)
async def travelagency(request: Request):
    return templates.TemplateResponse("travelagency.html", {"request": request})


# travel agency post
@app.post("/travelagency", response_class=HTMLResponse)
async def travelagency_dash(request: Request):
    # sample agency
    agency = {
        "id": 1,
        "name": "Bob's Agency",
        "users": [
            {"name" : "Stanley Parks","email" : "stanleyparks@gmail.com", "phone": "083 555 6733", "location" : "Sydney, Australia","destination" : "Bangkok, Thailand"}, 
            {"name" : "Edgar Wright","email" : "ewright@gmail.com", "phone": "074 555 1491", "location" : "Birmingham, England","destination" : "Swansea, Wales"},
            {"name" : "Jon Jones","email" : "jjones@gmail.com", "phone": "084 555 4143", "location" : "Manchester, England","destination" : "Durban, South Africa"},
            {"name" : "Maria de Souza","email" : "mdsouza@gmail.com", "phone": "073 555 3921", "location" : "Toronto, Canada","destination" : "Washington, USA"},
            {"name" : "Sibusiso Jacob","email" : "sjakes@gmail.com", "phone": "074 555 8127", "location" : "Cape Town, South Africa","destination" : "Windhoek, Namibia"}
        ],
        "phone": "555-5555-555",
        "locations": ["Sydney"],
        "email" : "bobsagency@gmail.com",
        "password" : "abc123",
        "new_requests" : [
            {"email": "garrysmith@gmail.com", "message": "I nned help booking a family vacation to the Caribbean."},
            {"email": "jamesdaniels@gmail.com", "message": "I would like to travel to Amsterdam from Manchester"}
        ],
        "current_requests": [
            {"name": "Stanley Parks", "message": "The hotel room was not booked. I need a new room."},
            {"name": "Jon Jones", "message": "Could you please postpone my flight by two weeks?"}
        ]
    }
    return templates.TemplateResponse("travelagency.html", {"request": request, "agency": agency})

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
