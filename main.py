import base64
import os
from typing import Optional, Annotated

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

import model
from database.handler import userdb
from database.handler.imagedb import select_image_by_email
from util.upload import upload_image

load_dotenv()
jwt_secret = os.getenv('JWT_SECRET')
jwt_algorithm = os.getenv('JWT_ALGORITHM')

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/signup")
async def signup(data: model.UserModel):
    userdb.insert_user((data.name, data.email, data.password))
    return {"message": "User created"}


@app.post("/login")
async def login(from_data: OAuth2PasswordRequestForm = Depends()) -> model.Token:
    if not userdb.select_user_by_email(from_data.username):
        raise HTTPException(status_code=422, detail="Invalid email or password")
    elif from_data.password != userdb.select_password_by_email(from_data.username)[0]:
        raise HTTPException(status_code=422, detail="Invalid email or password")
    token = jwt.encode({"email": from_data.username}, jwt_secret, jwt_algorithm)
    return model.Token(access_token=token, token_type="bearer")


@app.post("/upload")
async def upload(token: Annotated[str, Depends(oauth2_scheme)], file: Optional[UploadFile] = File(None)):
    user_data = jwt.decode(token, jwt_secret, jwt_algorithm)
    result = await upload_image(user_data['email'], file)
    return result


@app.post("/process")
async def process(token: Annotated[str, Depends(oauth2_scheme)]):
    user_data = jwt.decode(token, jwt_secret, jwt_algorithm)
    res = select_image_by_email(user_data['email'])
    img = base64.b64encode(res[0][2]).decode('utf-8')
    # todo: processing
    result = {
        "title": "AA 테스트 타이틀 123",
        "image": [img],
        "description": [],
        "date": "2024.04.21"
    }
    return result
