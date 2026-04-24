from pydantic import BaseModel, ConfigDict, Field

class postBase(BaseModel):
    author: str = Field(min_length=1, max_length = 100)
    content: str = Field(min_length=1, max_length=1000)
    title: str = Field(min_length=1, max_length=100)


class PostCreate(postBase):
    pass

class PostResponse(postBase):
    #from_attributes = True lets Pydantic read data from object attributes (using obj.title) instead of only dict keys (dict["title"]).
    model_config = ConfigDict(from_attributes=True)
    
    id :int
    date_posted: str