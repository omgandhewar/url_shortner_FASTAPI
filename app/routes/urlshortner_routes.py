from fastapi import FastAPI, APIRouter
from schemas.user import User
from services.urlshortner_services import user_urlshortner, user_urlredirect



router=APIRouter()


@router.post("/urlshortner")
def url_shortner(data:User):
    return user_urlshortner(data.Original_url)
 
 
@router.get("/urlredirect/{short_code}")
def url_redirect(short_code:str):
    return user_urlredirect(short_code)   