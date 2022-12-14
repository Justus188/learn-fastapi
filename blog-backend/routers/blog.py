from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import schemas, models
from auth.oauth2 import get_user_by_token

router = APIRouter(prefix = '/blog', tags = ['blogs'])

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.BlogOut)
def create(request: schemas.Blog, db: Session = Depends(get_db), user: models.User = Depends(get_user_by_token)):
    new_blog = models.Blog(**request.dict(), user_id = user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/', response_model = List[schemas.BlogOut])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()

@router.get('/{id}', response_model = schemas.BlogOut)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = {'detail': f'Blog with id {id} not found.'})
    return blog

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED, response_model = schemas.BlogOut)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), user: models.User = Depends(get_user_by_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = {'detail': f'Blog with id {id} not found.'})
    if blog.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = {'detail': "Unable to update others' post."})
    blog.update(request.dict())
    db.commit()
    return blog

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), user: models.User = Depends(get_user_by_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = {'detail': f'Blog with id {id} not found.'})
    if blog.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = {'detail': "Unable to delete others' post."})
    blog.delete()
    db.commit()