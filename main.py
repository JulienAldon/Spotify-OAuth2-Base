from secrets import origins, REDIRECT, ROOT_FQDN, CLIENT_ID, CLIENT_SECRET, SCOPES
from database import SessionLocal, engine, Base
from models import User

from fastapi import FastAPI, Header, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse

from typing import Optional, List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session

import requests
import json
import os
import base64

Base.metadata.create_all(bind=engine)

app = FastAPI()

SPOTIFY_API_ME = "https://api.spotify.com/v1/me"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(db: Session, spotify_id):
    db_user = User(spotify_id=spotify_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_spotify_id(db: Session, spotify_id: str):
    return db.query(User).filter(User.spotify_id == spotify_id).first()


@app.get('/api/auth/login')
async def spotify_api_login():
    return RedirectResponse(f'https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={SCOPES}&redirect_uri={REDIRECT}')

@app.get('/api/auth/authorized')
async def spotify_api_autorized(code: Optional[str] = None, db: Session = Depends(get_db)):
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': f'{REDIRECT}'
    }
    secret_string = CLIENT_ID + ':' + CLIENT_SECRET
    header = {
        'Authorization': b'Basic ' + base64.b64encode(secret_string.encode('utf-8')),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=header)
    res = r.json()
    token = res.get('access_token', None)
    if token is None:
        return RedirectResponse(f'{ROOT_FQDN}?token=None')
    me = requests.get(SPOTIFY_API_ME, headers={'Authorization': 'Bearer ' + token})
    res = me.json()
    db_user = get_user_by_spotify_id(db, spotify_id=res['id'])
    if db_user:
        result = r.json()
        token = result['access_token']
        return RedirectResponse(f'{ROOT_FQDN}?token={token}')
    create_user(db=db, spotify_id=res['id'])
    result = r.json()
    token = result['access_token']
    return RedirectResponse(f'{ROOT_FQDN}?token={token}')


@app.get('/api/auth/user')
async def read_user(authorization: Optional[str] = Header(None)):
    r = requests.get(SPOTIFY_API_ME, headers={'Authorization': authorization})
    user = r.json()
    user_id = user.get('id', None)
    user_name = user.get('display_name', None)
    if user_id is None or user_name is None:
        raise HTTPException(status_code=403, detail='No profile found, authorization token no more valid.')
    return {'username': user_name, 'id': user_id}