from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import schemas, models
from auth.hash import get_password_hash

router = APIRouter(prefix = '/user', tags = ['users'])

@router.post('/', status_code = status.HTTP_202_ACCEPTED, response_model = schemas.User)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check for duplicates
    dbUsers = db.query(models.User)
    if dbUsers.filter(models.User.username == request.username).first():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = {'detail': f'Username {request.username} already taken.'})
    if dbUsers.filter(models.User.email == request.email).first():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = {'detail': f'Email {request.email} already has an account. Please log in instead.'})
    # Create user
    request_dict = request.dict()
    request_dict['hashed_password'] = get_password_hash(request_dict.pop('password'))
    new_user = models.User(**request_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', response_model = List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get('/{id}', response_model = schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = {'detail': f'User with id {id} not found.'})
    return user