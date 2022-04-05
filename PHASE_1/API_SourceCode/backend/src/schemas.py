from typing import Optional
from datetime import datetime
from pydantic import BaseModel

##### Reports #####

class ReportBase(BaseModel):
    reportId: str
    eventDate: datetime

class ReportCreate(ArticleBase):
    pass

class Report(ReportBase):
    owner_id: str
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

##### Articles #####

class ArticleBase(BaseModel):
    articleId: str
    url: str
    dateOfPublication: datetime
    headline: str

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    reports: list[Report] = []

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

##### Diseases #####

class Disease(BaseModel):
    id: str
    name: str

    class Config:
        allow_population_by_field_name = True

class RepDisease(BaseModel):
    report: str
    disease: str
    
    class Config:
        allow_population_by_field_name = True

##### Syndromes #####

class Syndrome(BaseModel):
    id: str
    name: str
    
    class Config:
        allow_population_by_field_name = True

class RepSyndrome(BaseModel):
    report: str
    syndrome: str
    
    class Config:
        allow_population_by_field_name = True

##### Locations #####

class Location(BaseModel):
    id: str
    country: str
    location: str
    
    class Config:
        allow_population_by_field_name = True

class RepLocation(BaseModel):
    report: str
    location: str
    
    class Config:
        allow_population_by_field_name = True