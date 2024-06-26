

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()   # Instance of FastApi


'''
  .get is Operation
  @app is Path Operation Decorator
'''
# Decorators
@app.get('/')         
def index():    # Path Operation Function
    return {
        'data': {
            'name' : 'sarthak'
        }
    }
@app.get('/about')         
def index():    # Path Operation Function
    return {
        'data': {
            'about' : 'This is a about section'
        }
    }


'''
Path Parameters
'''
@app.get('/blogs/{id}')            # Dynamic Routing using FastApi   
def index(id):        # Accept path parameter here same name
    return {
        'data': {
            'id' : id
        }
    }

# This is never run either move up or change path or change id of above to int
@app.get('blogs/published')
def published():
    return

@app.get('/blogs/{id}/comments')
def index(id : int ):    # Typing Support using pydantic
    return {
        'data': [f'comment1 for id {id}','comment2']
    }

'''
Query Parameters
'''
@app.get('/blog/{id}')
def index(id,limit : int=10,published : bool=False,sort: Optional[str] = None):   # Accepting Query parameter as Validation
    
    if published:
        return { 'data': f'Limit = {limit} for published = {published} with id {id}'}
    else:
        return {'data': f'Limit = {limit} for published = {published}'}

'''
Request Body : From browser we cannot use post method so use Swagger doc. 
declare your data model as a class that inherits from BaseModel.
'''
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return { 'data' : f'blog is created with {request.title}'}


'''
Debugging FastApi --> Red Dot == breakpoint -- ur application stops there  ctrl + shift + p and choose debug
'''

# if __name__=="__main__":
#     uvicorn.run(app,host="127.0.0.1",port = 9000)


