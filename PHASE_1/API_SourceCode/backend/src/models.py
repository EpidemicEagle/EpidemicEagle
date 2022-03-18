from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    date = Column(String)
    headline = Column(String)
    maintext = Column(String)
    reports = Column(String)

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    diseases = Column(String)
    syndromes = Column(String)
    eventdate = Column(String)
    locations = Column(String)
    
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    location = Column(String)
    
    owner = relationship("User", back_populates="items")