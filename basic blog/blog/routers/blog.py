from fastapi import APIRouter,Depends
from typing import List
from .. import schema,models,database
from sqlalchemy.orm import Session


router = APIRouter()

@router.get('/blog',status_code=200,response_model=List[schema.ShowBlog],tags=["blogs"])
def get_all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs