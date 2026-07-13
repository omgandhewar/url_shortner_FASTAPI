from fastapi import FastAPI, Depends, Request, APIRouter
from schemas.user import User
from dependencies import get_current_user
from services.urlshortner_services import user_urlshortner, user_urlredirect, get_userurl, user_dashboard, user_Analytics



router=APIRouter()


@router.post("/urlshortner")
def url_shortner(data:User,current_user=Depends(get_current_user)):
    return user_urlshortner(data.Original_url,current_user)
 
 
@router.get("/urlredirect/{short_code}")
def url_redirect(request:Request,short_code:str,current_user=Depends(get_current_user)):
    return user_urlredirect(request,short_code)


@router.get("/geturl")
def get_url(search: str | None=None,page: int=1,limit: int=10,current_user=Depends(get_current_user)):
    return get_userurl(search,page,limit,current_user) 


@router.get("/Analytics/{url_id}")
def get_Analytics(url_id,current_user=Depends(get_current_user)):
    return user_Analytics(url_id,current_user)  


@router.get("/dashboard")
def dashboard(current_user=Depends(get_current_user)):
    return user_dashboard(current_user)