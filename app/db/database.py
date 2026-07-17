from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL="mysql+pymysql://root:root@localhost/url_shortner_Fastapi"

engine=create_engine(
    DATABASE_URL
)

sessionlocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()

def get_db():

    db = sessionlocal()

    try:
        yield db

    finally:
        db.close()

