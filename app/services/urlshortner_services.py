from fastapi import FastAPI, Request
from db.database import sessionlocal
from urllib.parse import urlparse
import random
import string

def generate_code(lenght=6):
    
    char=string.ascii_letters+string.digits
    return ''.join(random.choice(char) for _ in range(lenght))


def user_urlshortner(Original_url:str):
    db=sessionlocal()
    
