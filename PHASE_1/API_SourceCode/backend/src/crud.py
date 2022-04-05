from sqlalchemy.orm import Session

from . import models, schemas

def get_report(db: Session, report_id: str):
    return db.query(models.Report).filter(models.Report.id == report_id).first()

def get_reports(db: Session):
    return db.query(models.Report).all()

def create_report(db: Session):


def get_article(db: Session, article_id: str):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_articles(db: Session):
    return db.query(models.Article).all()

def search(db: Session, key_terms: str, location: str, start_date: datetime, end_date: datetime):
    # currently searching only on country
    locs = db.query(models.Location.id).filter(models.Location.country == location).subquery()
    locreports = db.query(models.RepLocation.report).filter(models.RepLocation.location.in_(locs)).subquery()
    terms = db.query(models.Disease.id).filter(models.Disease.name.match("%" + key_terms + "%")).subquery()
    termreports = db.query(models.RepDisease.report).filter(models.RepDisease.disease.in_(terms)).subquery().
    owners = db.query(models.Report.owner).filter(models.Report.id.in_(reports)).subquery()
    return db.query(models.Article.id, models.Article.url, models.Article.date, models.Article.headline).filter\
    models.Article.date.between(start_date, end_date), models.Article.id.in_(owners))