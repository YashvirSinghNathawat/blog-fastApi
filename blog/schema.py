# Schema to accept request body
from pydantic import BaseModel
class Blog(BaseModel):
    title: str
    body: str