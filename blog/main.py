from fastapi import FastAPI,Depends
from . import schema,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session

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
@app.post('/blog')
def create(request: schema.Blog,db : Session = Depends(get_db)):  # Depend to handle the dependency and db is db instance
    new_blog = models.Blog(title = request.title,body=request.body)  # SQLAlchemy Model instance
    db.add(new_blog)       # Add instance object to database session
    db.commit()           # Commit changes to database
    db.refresh(new_blog)   # Refresh so that it contains any new data
    return new_blog


@app.get('/blog')
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def get_blog(id : int,db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id==id).first()
    return blogs
