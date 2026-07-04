from fastapi import FastAPI, Request, Depends, APIRouter
from services.auth_services import user_signup, user_login, user_refreshtoken, user_logout
from fastapi.responses import JSONResponse
from dependencies import get_current_user
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

@auth_router.post("/refresh")
def refresh(request:Request):
    return user_refreshtoken(request.cookies.get("refresh_token"))

@auth_router.post("/logout")
def logout(request:Request):
    return user_logout(request.cookies.get("refresh_token"))

@auth_router.get("/dashboard")
def dashboard(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.username,
        "email": current_user.email
    }
