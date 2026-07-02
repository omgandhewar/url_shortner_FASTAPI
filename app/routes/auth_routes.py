from fastapi import FastAPI, APIRouter


auth_router=APIRouter()

@auth_router.post("/login")
def login():
    return user_login()