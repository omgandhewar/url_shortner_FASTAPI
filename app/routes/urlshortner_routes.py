from fastapi import FastAPI, Depends, Request, APIRouter
from schemas.user import User
from dependencies import get_current_user
from services.urlshortner_services import user_urlshortner, user_urlredirect, get_userurl, user_dashboard



router=APIRouter()


@router.post("/urlshortner")
def url_shortner(data:User,current_user=Depends(get_current_user)):
    return user_urlshortner(data.Original_url,current_user)
 
 
@router.get("/urlredirect/{short_code}")
def url_redirect(request:Request,short_code:str,current_user=Depends(get_current_user)):
    return user_urlredirect(request,short_code)


@router.get("/geturl")
def get_url(current_user=Depends(get_current_user)):
    return get_userurl(current_user)   


@router.get("/dashboard")
def dashboard(current_user=Depends(get_current_user)):
    return user_dashboard(current_user)