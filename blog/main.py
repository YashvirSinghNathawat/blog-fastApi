from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import schema,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

# Create Table
models.Base.metadata.create_all(engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



'''
SQL Alchemy is Python SQL tootkit and Object Relational Mapper(ORM) Maps Pet
could represent a SQL table pets. Each instance of that class represents a row in
the database

db should be type Session but Session is not part of pydantic rather part of sql.orm
One session for each database operation
'''
@app.post('/blog',status_code=201)
def create(request: schema.Blog,db : Session = Depends(get_db)):  # Depend to handle the dependency and db is db instance     #schema to provide request body
    new_blog = models.Blog(title = request.title,body=request.body)  # SQLAlchemy Model instance
    db.add(new_blog)       # Add instance object to database session
    db.commit()           # Commit changes to database
    db.refresh(new_blog)   # Refresh so that it contains any new data

    return new_blog


@app.get('/blog',status_code=200,response_model=List[schema.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',response_model=schema.ShowBlog)
def get_blog(id : int,response: Response,db: Session = Depends(get_db) ):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:                                          # Custom response using FastApi response
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id={id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail' : f'Blog with id={id} is not available'}
    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id : int,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"Blog with id={id} not found")
    blog.delete(synchronize_session=False)
    # Whenever we do something on db we need to commit the changes
    db.commit()
    return {'message':'Deleted Successfully!!'}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id : int, request : schema.Blog, db : Session = Depends(get_db)):
    new_blog = {
        'title': request.title,
        'body': request.body
    }
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"Blog with id={id} not found")
    blog.update(new_blog,synchronize_session=False)
    db.commit()
    return {'message':'Updated Successfully!!'}
