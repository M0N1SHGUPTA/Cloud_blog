from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_legth = 50)
    email: str = Field(min_lenght=1, max_length = 50)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    #from_attributes = True lets Pydantic read data from object attributes (using obj.title) instead of only dict keys (dict["title"]).
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_file: str | None
    image_path: str


class postBase(BaseModel):
    author: str = Field(min_length=1, max_length = 100)
    content: str = Field(min_length=1, max_length=1000)
    title: str = Field(min_length=1, max_length=100)


class PostCreate(postBase):
    user_id: int #temprory

class PostResponse(postBase):
    #from_attributes = True lets Pydantic read data from object attributes (using obj.title) instead of only dict keys (dict["title"]).
    model_config = ConfigDict(from_attributes=True)
    
    id :int
    user_id: int
    date_posted: datetime
    author: UserResponse