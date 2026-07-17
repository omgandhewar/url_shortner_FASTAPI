from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy import text
from fastapi.responses import RedirectResponse
import validators
from urllib.parse import urlparse
import random
import string

def generate_code(lenght=6):
    
    char=string.ascii_letters+string.digits
    return ''.join(random.choice(char) for _ in range(lenght))


def user_urlshortner(Original_url:str,current_user,db):
    
    user_id=current_user[0]
    
    parsedurl=urlparse(Original_url)
    
    print(parsedurl)
    
    if not parsedurl.scheme or not parsedurl.netloc:
        raise HTTPException(status_code=422,detail="Invalid url")
        
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
    
    
def user_urlredirect(request,short_code,db):
    
    print({
    "short_code": short_code
})
    
    result=db.execute(
        text("SELECT id,short_code,Original_url,Count_click FROM url_shortner WHERE short_code=:short_code"),
        {
            "short_code":short_code
        }
    )
    
    short_url=result.fetchone()
    
    
    if not short_url:
        return{
            "message":"url not available"
        }
      
      
    url_id=short_url[0]    
    Original_url=short_url[2]
    Count_click=short_url[3]    
    
    db.execute(
        text("INSERT INTO Click_url(url_id,ip_address,user_agent) VALUES(:url_id,:ip_address,:user_agent)"),
        {
            "url_id":url_id,
            "ip_address":request.client.host,
            "user_agent":request.headers.get("User-Agent")
        }
    )
    
    db.commit()
    
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


def get_userurl(search,page,limit,current_user,db):
    
    offset=(page-1)*limit
    
    if search is None:
        result=db.execute(
        text("SELECT id,short_code,Original_url,Count_click FROM url_shortner WHERE user_id=:current_user LIMIT:limit,OFFSET:offset"),
        {
            "current_user":current_user.id,
            "limit":limit,
            "offset":offset
        }
    )
    else:
         result=db.execute(
        text("SELECT id,short_code,Original_url,Count_click FROM url_shortner WHERE user_id=:current_user AND Original_url LIKE :search LIMIT:limit,OFFSET:offset"),
        {
            "current_user":current_user.id,
            "search":f"%{search}%",
            "limit":limit,
            "offset":offset
        }
    )

    user_url=result.mappings().first()
    
    if not user_url:
        return{
            "message":"url not found"
        }
    
    return{
        "url":user_url
    }
    
    
def user_Analytics(url_id,current_user,db):
    
    result=db.execute(
        text("SELECT id FROM url_shortner WHERE id=:url_id AND user_id=:current_user"),
        {
            "url_id":url_id,
            "current_user":current_user.id
        }
    )
    
    user=result.mappings().first()
    
    print(user)
    
    if not user:
        raise HTTPException(status_code=403,detail="short url are not available")
    
    result=db.execute(
        text("SELECT COUNT(*),MAX(clicked_at) FROM Click_url WHERE url_id=:url_id"),
        {
            "url_id":user["id"]
        }
    )
    
    user_obj=result.fetchone()
    
    total_clicked=user_obj[0]
    last_clicked=user_obj[1]
    
    return{
        "total_clicked":total_clicked,
        "Last_clciked":last_clicked
    }
    
    
def user_dashboard(current_user,db):
    
    result=db.execute(
        text("SELECT COUNT(Original_url) AS total_url,SUM(Count_click) AS total_count FROM url_shortner WHERE user_id=:current_user"),
        {
            "current_user":current_user.id
        }
    )
    
    user=result.mappings().first()
    
    return{
        "total_url":user["total_url"],
        "total_count":user["total_count"]
    }