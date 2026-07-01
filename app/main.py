from fastapi import FastAPI
from db.database import Base, engine


def create_app():
    
    app=FastAPI()


    Base.metadata.create_all(bind=engine)

    return app

app=create_app()


