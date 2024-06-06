# Schema to accept request body
from pydantic import BaseModel

# We have 2 models pydantic models(these are schemas) and sql models
class Blog(BaseModel):
    title: str
    body: str

# Schema model for response we dont user to see id
class ShowBlog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    password: str
    email: str

class ShowUser(BaseModel):
    name: str
    email: str