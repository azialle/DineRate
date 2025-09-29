from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.schema import Base

engine = create_engine("sqlite:///instance/dinerate.db")
Base.metadata.create_all(engine)


def get_session():
    return Session(engine)
