from fastapi import FastAPI, Depends, APIRouter
from schemas.user import User
from dependencies import get_current_user
from services.urlshortner_services import user_urlshortner, user_urlredirect



router=APIRouter()


@router.post("/urlshortner")
def url_shortner(data:User,current_user=Depends(get_current_user)):
    return user_urlshortner(data.Original_url,current_user)
 
 
@router.get("/urlredirect/{short_code}")
def url_redirect(short_code:str,current_user=Depends(get_current_user)):
    return user_urlredirect(short_code,current_user)   