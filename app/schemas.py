from pydantic import BaseModel,EmailStr
from datetime import datetime
from pydantic.types import conint
from typing import Optional
# Dependency
# base
class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True
    

# for create and update a user
class CreatePost(BasePost):
    pass


# for user response
class UserOut(BaseModel):
    id:int
    email:EmailStr  
    created_at:datetime

    
    class Config:
        orm_mode=True

# for response
class PostResponse(BasePost):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    
    class Config:
        orm_mode=True

# for post owner and vote
class PostOut(BasePost):
    Post:PostResponse
    votes:int
    
    class Config:
        orm_mode=True
    
# for user creation
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    



    

# login

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
    
    
# token

class Token(BaseModel):
    access_token:str
    token_type:str
    
# token data

class TokenData(BaseModel):
    id:Optional[int]=None
    
    
# voting
class Vote(BaseModel):
    post_id:int
    vote_dir:conint(ge=0,le=1)
    