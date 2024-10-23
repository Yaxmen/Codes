import sys
import logging
import uvicorn

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from Hash import get_rand_hash
from Security import get_password_hash
from ConexãoBDEx import DBConnectionHandler
from ModelosEx import Tb_order
from typing import List
from EsquemasEx import OrderSchema
from ModelosEx import User
from typing import List
from EsquemasEx import UserChangeStatusSchema, UserCreateSchema, UserListSchema, UserOutSchema, UserUpdateSchema

logger = logging.getLogger(__name__)
app = FastAPI()

# Rotas.
@app.get("/user/{id}", response_model=UserOutSchema)
def get_user(id: str):
    try:
        with DBConnectionHandler() as db:
            user = db.session.query(User).filter(User.pk_user == id).first()
            if user:
                return user
            else:
                raise HTTPException(status_code=404, detail=f"User with ID {id} not found.")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@app.get("/user", response_model=List[UserListSchema])
def list_users(skip: int = 0, limit: int = 10):
    try:
        with DBConnectionHandler() as db:
            users = db.session.query(User).offset(skip).limit(limit).all()
            return users
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@app.post("/user", response_model=UserOutSchema)
def create_user(user: UserCreateSchema):
    try:
        with DBConnectionHandler() as db:
            user_data = user.model_dump()
            user_data['is_active'] = True
            user_data['is_employee'] = True
            user_data["user_token"] = get_rand_hash()
            user_data["password"] = get_password_hash(user.password)
            
            new_user = User(**user_data)
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            return new_user
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@app.put("/user/{id}", response_model=UserOutSchema)
def update_user(id: str, user: UserUpdateSchema):
    try:
        user_data = user.model_dump()
        with DBConnectionHandler() as db:
            db_user = db.session.query(User).filter(User.pk_user == id).first()
            if db_user:
                user_data['password'] = db_user.password
                for key, value in user_data.items():
                    setattr(db_user, key, value)
                db.session.commit()
                db.session.refresh(db_user)
                return db_user
            else:
                raise HTTPException(status_code=404, detail=f"User with ID {id} not found.")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@app.put("/user/{id}/change_status", status_code=200)
def change_status_user(id: str, user_status: UserChangeStatusSchema):
    try:
        with DBConnectionHandler() as db:
            db_user = db.session.query(User).filter(User.pk_user == id).first()
            if db_user:
                db_user.is_active = user_status.model_dump().get('is_active')
                db.session.commit()
                return
            else:
                raise HTTPException(status_code=404, detail=f"User with ID {id} not found.")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.delete("/user/{id}", status_code=204)
def delete_user(id: str):
    try:
        with DBConnectionHandler() as db:
            db_user = db.session.query(User).filter(User.pk_user == id).first()
            if db_user:
                db.session.delete(db_user)
                db.session.commit()
                return
            else:
                raise HTTPException(status_code=404, detail=f"User with ID {id} not found.")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
        
if __name__ == '__main__':

    # identificação de migrations
    if 'makemigrations' in sys.argv:
        with DBConnectionHandler() as db:
            db.check_db_structure()
        sys.exit()
    

    uvicorn.run('app:app', host="0.0.0.0", port=8000, log_config='./logging.conf.yml', reload=True)





