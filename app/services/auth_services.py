from fastapi import FastAPI, HTTPException
from db.database import sessionlocal
from utils.jwt import create_access_token, create_refresh_token
from sqlalchemy import text
from utils.password import hashed_password, verify_password




def user_signup(user):
    db=sessionlocal()
    
    name=user.name
    email=user.email
    password=user.password
    
    result=db.execute(
        text("SELECT email FROM users WHERE email=:email"),
        {
            "email":email
        }
    )
    
    user_obj=result.fetchone()
    
    if user_obj:
        return{
            "message":"user already exists"
        }
        
    hashed_passsword1=hashed_password(password)
    
    db.execute(
        text("INSERT INTO users(username,email,password) VALUES(:name,:email,:password)"),
        {
            "name":name,
            "email":email,
            "password":hashed_passsword1
        }
    )
    
    db.commit()
    
    return{
        "message":"user added successfully"
    }
    
    
def user_login(user):
    db=sessionlocal()
    
    email=user.email,
    password=user.password
    
    if not email or not password:
        raise HTTPException(
        status_code=400,
        detail="email and password are required"
    )
        
    result=db.execute(
        text("SELECT id,email,password FROM users WHERE email=:email"),
        {
            "email":email
        }
    )
    
    user_obj=result.fetchone()
    
    if not user_obj:
        raise HTTPException(
            status_code=401,
            detail="invalid credential"
        )
        
    is_valid=verify_password(
        password,
        user_obj.password
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="invalid credential"
        )
    
    access_token=create_access_token({
        "user_id":user_obj.id
    })
    
    refresh_token=create_refresh_token({
        "user_id":user_obj.id
    })
    
    return{
        "message":"login successful",
        "access_token":access_token,
        "refresh_token":refresh_token        
    }
    
    