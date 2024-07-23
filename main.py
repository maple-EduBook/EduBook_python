from fastapi import FastAPI, HTTPException
import model
import db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/signup")
async def signup(data: model.UserModel):
    db.insert_user((data.name, data.email, data.password))
    return {"message": "User created"}


@app.post("/login")
async def login(data: model.UserLoginModel):
    if not db.select_user_by_email(data.email):
        raise HTTPException(status_code=422, detail="Invalid email or password")
    elif data.password != db.select_password_by_email(data.email)[0]:
        raise HTTPException(status_code=422, detail="Invalid email or password")
    return {"message": "User logged in"}