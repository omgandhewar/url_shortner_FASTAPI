from fastapi import FastAPI, APIRouter
from services.auth_services import user_signup, user_login
from fastapi.responses import JSONResponse
from schemas.user import usersignup, userlogin


auth_router=APIRouter()



@auth_router.post("/signup")
def signup(user:usersignup):
    return user_signup(user)

@auth_router.post("/login")
def login(user:userlogin):
    token=user_login(user)
    
    response=JSONResponse(
        content={
            "message":"login successfull"
        }
    )
    
    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        httponly=True
    )
    
    response.set_cookie(
        key="refresh_token",
        value=token["refresh_token"],
        httponly=True
    )
    
    return response


    