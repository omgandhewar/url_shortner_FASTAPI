from fastapi import FastAPI, Request, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy import text
from db.database import get_db
from utils.jwt import SECRET_KEY, ALGORITHM


def get_current_user(request:Request,db=Depends(get_db)):
    
    token=request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=401,detail="Not Authenticated")
    
    try:
        paylaod=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        user_id=paylaod.get("user_id")
        
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
            
    except JWTError:
        
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )
        
    
    result=db.execute(
        text("SELECT * FROM users WHERE id=:user_id"),
        {
            "user_id":user_id
        }
    )
    
    user=result.fetchone()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="user not found"
        )
        
    return user
  
    