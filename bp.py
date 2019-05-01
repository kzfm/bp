# -*- coding: utf-8 -*- 

from io import BytesIO
import click
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Index
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

database_file = os.path.join(os.path.abspath(os.path.expanduser('~')), 'mybp.db')
database_uri = 'sqlite:///' + database_file
engine = create_engine(database_uri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class BloodPressure(Base):
    __tablename__ = 'bp'
    id = Column(Integer, primary_key=True)
    diastolic = Column(Integer, nullable=False)
    systolic = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, **k):
        self.diastolic =k["diastolic"]
        self.systolic =k["systolic"]

def init():
    Base.metadata.create_all(bind=engine)

@click.command()
@click.argument("n1")
@click.argument("n2")
def cmd(n1, n2):
    if n2 > n1:
        sys = n2
        dia = n1
    else:
        sys = n1
        dia = n2
    bp = BloodPressure(diastolic=dia, systolic=sys)
    db_session.add(bp)
    db_session.commit()


if __name__ == "__main__":
    cmd()