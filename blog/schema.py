# Schema to accept request body
from pydantic import BaseModel
from typing import List

# We have 2 models pydantic models(these are schemas) and sql models

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    password: str
    email: str

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]    # This should be same as relationship we created
    class Config():
        orm_mode = True

# Schema model for response we dont user to see id
class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    class Config():
        orm_mode = True