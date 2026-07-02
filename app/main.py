from fastapi import FastAPI
from db.database import Base, engine
from routes.urlshortner_routes import router


def create_app():
    
    app=FastAPI()


    app.include_router(router)

    Base.metadata.create_all(bind=engine)

    return app

app=create_app()


