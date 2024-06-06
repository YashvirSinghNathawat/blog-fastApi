from fastapi import FastAPI
from . import schema

app = FastAPI()



'''
SQL Alchemy is Python SQL tootkit and Object Relational Mapper(ORM) Maps Pet
could represent a SQL table pets. Each instance of that class represents a row in
the database
'''


@app.post('/blog')
def create(request: schema.Blog):
    return 'creating'