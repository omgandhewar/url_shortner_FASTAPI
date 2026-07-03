from fastapi import FastAPI
from db.database import Base, engine
from routes.urlshortner_routes import router
from routes.auth_routes import auth_router


def create_app():
    
    app=FastAPI()


    app.include_router(router)
    app.include_router(auth_router)

    Base.metadata.create_all(bind=engine)

    return app

app=create_app()


