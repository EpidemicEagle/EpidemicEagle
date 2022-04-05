from sqlalchemy import Column, ForeignKey, String, DateTime, Index
from sqlalchemy.orm import relationship

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    articleId = Column(String, primary_key=True, index=True)
    url = Column(String)
    dateOfPublication = Column(DateTime, index=True)
    headline = Column(String)
    
    reports = relationship("Report", back_populates="owner")

class Report(Base):
    __tablename__ = "reports"

    reportId = Column(String, primary_key=True, index=True)
    eventDate = Column(DateTime, index=True)

    owner = relationship("Article", back_populates="reports")

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)

class RepDisease(Base):
    __tablename__ = "report_diseases"

    report = Column(String, ForeignKey("reports.id"), primary_key=True)
    disease = Column(String, ForeignKey("diseases.id"), primary_key=True)

class Syndrome(Base):
    __tablename__ = "syndromes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)

class RepSyndrome(Base):
    __tablename__ = "report_syndromes"

    report = Column(String, ForeignKey("reports.id"), primary_key=True)
    syndrome = Column(String, ForeignKey("syndromes.id"), primary_key=True)

class Location(Base):
    __tablename__ = "locations"

    id = Column(String, primary_key=True, index=True)
    country = Column(String, index=True)
    location = Column(String, index=True)

class RepLocation(Base):
    __tablename__ = "report_locations"

    report = Column(String, ForeignKey("reports.id"), primary_key=True)
    location = Column(String, ForeignKey("locations.id"), primary_key=True)