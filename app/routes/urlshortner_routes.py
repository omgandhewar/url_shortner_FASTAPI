from fastapi import FastAPI, APIRouter
from schemas.user import User



router=APIRouter()


@router.post("/urlshortner")
def url_shortner(data:User):
    return user_urlshortner(data.Original_url)
    