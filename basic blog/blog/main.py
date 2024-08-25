from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import schema,models
from .database import engine,get_db
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import blog

app = FastAPI()

# Create Table
models.Base.metadata.create_all(engine)

#Include routes
app.include_router(blog.router)





'''
SQL Alchemy is Python SQL tootkit and Object Relational Mapper(ORM) Maps Pet
could represent a SQL table pets. Each instance of that class represents a row in
the database

db should be type Session but Session is not part of pydantic rather part of sql.orm
One session for each database operation
'''
@app.post('/blog',status_code=201,tags=["blogs"])
def create(request: schema.Blog,db : Session = Depends(get_db)):  # Depend to handle the dependency and db is db instance     #schema to provide request body
    new_blog = models.Blog(title = request.title,body=request.body,user_id = 1)  # SQLAlchemy Model instance
    db.add(new_blog)       # Add instance object to database session
    db.commit()           # Commit changes to database
    db.refresh(new_blog)   # Refresh so that it contains any new data
    return new_blog




@app.get('/blog/{id}',response_model=schema.ShowBlog,tags=["blogs"])
def get_blog(id : int,response: Response,db: Session = Depends(get_db) ):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:                                          # Custom response using FastApi response
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id={id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail' : f'Blog with id={id} is not available'}
    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["blogs"])
def delete_blog(id : int,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"Blog with id={id} not found")
    blog.delete(synchronize_session=False)
    # Whenever we do something on db we need to commit the changes
    db.commit()
    return {'message':'Deleted Successfully!!'}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
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

'''User Endpoint'''

@app.post('/create-user',status_code=201,response_model=schema.ShowUser,tags=["users"])
def create_user(request: schema.User,db : Session = Depends(get_db)):
    # Hashing the password
    hashed_password = Hash.get_hashed_password(request.password)
    new_user = models.User(name = request.name,password = hashed_password, email = request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',status_code=200,response_model=schema.ShowUser,tags=["users"] )
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"User with id={id} not found")
    return user

