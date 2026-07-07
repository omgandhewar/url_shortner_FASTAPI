from fastapi import FastAPI, Request 
from db.database import sessionlocal
from sqlalchemy import text
from fastapi.responses import RedirectResponse
import validators
from urllib.parse import urlparse
import random
import string

def generate_code(lenght=6):
    
    char=string.ascii_letters+string.digits
    return ''.join(random.choice(char) for _ in range(lenght))


def user_urlshortner(Original_url:str,current_user):
    db=sessionlocal()
    
    user_id=current_user[0]
    
    parsedurl=urlparse(Original_url)
    
    print(parsedurl)
    
    if not parsedurl.scheme or not parsedurl.netloc:
        return{
            "message":"invalid url"
        }
        
    if not validators.url(Original_url):
        return{
            "message":"invalid url"
        }
        
    short_code=generate_code()
    
    db.execute(
        text("INSERT INTO url_shortner(user_id,short_code,Original_url) VALUES(:user_id,:short_code,:Original_url)"),
    {
        "user_id":user_id,
        "short_code":short_code,
        "Original_url":Original_url
    }
    )
    db.commit()
    
    return{
        "message":"short code"
    }
    
    
def user_urlredirect(short_code):
    db=sessionlocal()
    
    result=db.execute(
        text("SELECT short_code,Original_url,Count_click FROM url_shortner WHERE short_code=:short_code"),
        {
            "short_code":short_code
        }
    )
    
    short_url=result.fetchone()
    
    if not short_url:
        return{
            "message":"url not available"
        }
        
    Original_url=short_url[1]
    Count_click=short_url[2]
    
    Count_click+=1
    
    db.execute(
        text("UPDATE url_shortner SET count_click=:Count_click WHERE short_code=:short_code"),
        {
            "Count_click":Count_click,
            "short_code":short_code            
        }
    )
    
    db.commit()
    
    return RedirectResponse(Original_url)