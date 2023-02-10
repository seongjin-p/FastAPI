import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from datetime import datetime
from typing import List, Optional

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


class Pro_Req(BaseModel):
    SEMESTER: str
    EXAM_KIND: str
    SUBJECT: str
    TITLE: str
    ANSWER: int
    IMPORTANT: str
    TRIAL: int
    CORRECTION: int


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

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


app = FastAPI()


@app.get('/pros', response_model=List[ProBase])
async def get_pros(db: Session = Depends(get_db)):
    pros = db.query(Pro).all()
    return pros


@app.post('/pros', response_model=ProBase)
async def register_pro(req: Pro_Req, db: Session = Depends(get_db)):
    pro = Pro(**req.dict())
    db.add(pro)
    db.commit()
    return pro


@app.delete('/pros/{item_id}')
async def del_pro(item_id: str, db: Session = Depends(get_db)):
    pro = db.query(Pro).filter_by(id=item_id).first()
    db.delete(pro)
    db.commit()
    return pro


@app.put('/pros/{item_id}', response_model=ProBase)
async def mod_pro(item_id: str, req: Pro_Req, db: Session = Depends(get_db)):
    pro = db.query(Pro).filter_by(id=item_id)
    req_dict = req.dict()
    req_dict['id'] = item_id
    req = {k: v for k, v in req_dict.items()}
    for key, value in req.items():
        setattr(pro, key, value)
    db.commit()
    return pro
