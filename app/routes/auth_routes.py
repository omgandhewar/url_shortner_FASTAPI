from fastapi import FastAPI, APIRouter


auth_router=APIRouter()



@auth_router.post("/signup")
def signup():
    return user_signup()

@auth_router.post("/login")
def login():
    return user_login()