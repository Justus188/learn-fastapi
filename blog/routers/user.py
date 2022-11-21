from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models
from database import get_db
from auth.hash import get_password_hash

router = APIRouter(prefix = '/user', tags = ['users'])

@router.post('/', status_code = status.HTTP_202_ACCEPTED, response_model = schemas.User)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    request_dict = request.dict()
    request_dict['hashed_password'] = get_password_hash(request_dict.pop('password'))
    new_user = models.User(**request_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model = schemas.User)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = {'detail': f'User with id {id} not found.'})
    return user