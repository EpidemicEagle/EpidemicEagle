from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
host_server = "ec2-34-224-226-38.compute-1.amazonaws.com"
db_server_port = "5432"
database_name = "desonmrfnutlcj"
db_username = "jvbdmeujomzjxw"
db_password = "9a5944804411f74cf2c008dde4507f42b600cde4ef7bf93a9ccc895a12066bc6"

SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(db_username, db_password, host_server, db_server_port, database_name)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()