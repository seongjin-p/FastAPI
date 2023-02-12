import uuid
import base64
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from datetime import datetime
from typing import List, Optional
from base64 import b64encode, b64decode

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://seongjin:0629@localhost/testdb"
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Base.metadata.bind = engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        raise HTTPException(status_code=400, detail="DB와 연결에 실패하였습니다.")
    finally:
        db.close()


class Pro(Base):
    __tablename__ = 'problems'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    SEMESTER = Column(String, nullable=False)
    EXAM_KIND = Column(String, nullable=False)
    SUBJECT = Column(String, nullable=False)
    TITLE = Column(String, nullable=False)
    ANSWER = Column(Integer, nullable=False)
    IMPORTANT = Column(String, nullable=False)
    TRIAL = Column(Integer, nullable=False)
    CORRECTION = Column(Integer, nullable=False)
    IMAGE_PATH = Column(String, nullable=False)


class Pro_Req(BaseModel):
    SEMESTER: str
    EXAM_KIND: str
    SUBJECT: str
    TITLE: str
    ANSWER: int
    IMPORTANT: str
    TRIAL: int
    CORRECTION: int
    IMAGE_PATH: str


class ProBase(BaseModel):
    id: str
    SEMESTER: str
    EXAM_KIND: str
    SUBJECT: str
    TITLE: str
    ANSWER: int
    IMPORTANT: str
    TRIAL: int
    CORRECTION: int
    IMAGE_PATH: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


app = FastAPI()


@app.get('/pros', response_model=List[ProBase])
async def get_pros(db: Session = Depends(get_db)):
    pros = db.query(Pro).all()
    if pros is None:
        raise HTTPException(status_code=400, detail="DB와 연결에 실패하였습니다.")
    return pros


@app.get('/pros/{item_id}', response_model=List[ProBase])
async def get_pro(item_id: str, db: Session = Depends(get_db)):
    pro = db.query(Pro).filter_by(id=item_id).first()
    if os.path(pro.IMAGE_PATH) == False:
        raise HTTPException(status_code=400, detail="이미지가 확인되지 않습니다.")
    else:
        if pro is None:
            raise HTTPException(status_code=400, detail="DB와 연결에 실패하였습니다.")
        else:
            return pro


@app.post('/pros', response_model=ProBase)
async def register_pro(req: Pro_Req, db: Session = Depends(get_db)):
    if os.path.isfile(req.IMAGE_PATH) == False:
        raise HTTPException(status_code=400, detail="이미지가 확인되지 않습니다.")
    else:
        pro = Pro(**req.dict())
        try:
            db.add(pro)
        except:
            raise HTTPException(status_code=400, detail="DB와 연결에 실패하였습니다.")
            os.remove(req.IMAGE_PATH)
        db.commit()
        return pro


@app.delete('/pros/{item_id}')
async def del_pro(item_id: str, db: Session = Depends(get_db)):
    pro = db.query(Pro).filter_by(id=item_id).first()
    os.remove(pro.IMAGE_PATH)
    db.delete(pro)
    db.commit()
    if pro is None:
        raise HTTPException(status_code=400, detail="DB와 연결에 실패하였습니다.")
    else:
        return pro


@app.put('/pros/{item_id}', response_model=ProBase)
async def mod_pro(item_id: str, req: Pro_Req, db: Session = Depends(get_db)):
    if os.path.isfile(req.IMAGE_PATH) == False:
        raise HTTPException(status_code=400, detail="이미지가 확인되지 않습니다.")
    else:
        pro = db.query(Pro).filter_by(id=item_id).first()
        os.remove(pro.IMAGE_PATH)
        req_dict = req.dict()
        req_dict['id'] = item_id
        req = {k: v for k, v in req_dict.items()}
        for key, value in req.items():
            setattr(pro, key, value)
        db.commit()
        if pro is None:
            raise HTTPException(status_code=400, detail="DB와 연결에 실패하였습니다.")
            os.remove(req.IMAGE_PATH)
        else:
            return pro
