from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .properties import properties

p_ = properties()


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{p_.USERNAME}:{p_.USERPASSWORD}@{p_.DB_SERVER}/{p_.DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL # , connect_args={"check_same_thread": False} only used for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()