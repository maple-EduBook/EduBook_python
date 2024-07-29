from pydantic import BaseModel, field_validator
import re

from database.handler import userdb


class UserModel(BaseModel):
    name: str
    email: str
    password: str

    @field_validator('*')
    @classmethod
    def is_empty(cls, v: str) -> str:
        if v == "":
            raise ValueError('Field cannot be empty')
        return v

    @field_validator('email')
    @classmethod
    def is_valid_email(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError('Invalid email format')
        if userdb.select_user_by_email(v):
            raise ValueError('Email already exists')
        return v


class UserLoginModel(BaseModel):
    email: str
    password: str

    @field_validator('*')
    @classmethod
    def is_empty(cls, v: str) -> str:
        if v == "":
            raise ValueError('Field cannot be empty')
        return v


class Token(BaseModel):
    access_token: str
    token_type: str
