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
        self.diastolic = k["diastolic"]
        self.systolic = k["systolic"]


@click.group()
def cmd():
    pass

@cmd.command()
def init():
    Base.metadata.create_all(bind=engine)

@cmd.command()
@click.argument("n1", type=int)
@click.argument("n2", type=int)
def add(n1, n2):
    if n2 > n1:
        sys = n2
        dia = n1
    else:
        sys = n1
        dia = n2
    bp = BloodPressure(diastolic=dia, systolic=sys)
    db_session.add(bp)
    db_session.commit()

@cmd.command()
def show():
    import seaborn as sns
    import pandas as pd
    from matplotlib import pyplot as plt
    sns.set(style="darkgrid")
    df = pd.read_sql_query(sql="SELECT date, diastolic, systolic from bp", con=engine)
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="date", y="diastolic")
    sns.lineplot(data=df, x="date", y="systolic")
    fig.autofmt_xdate()
    plt.show()


@cmd.command()
def list():
    for bp in BloodPressure.query.order_by(BloodPressure.date.desc()).limit(30):
        print("{0:%Y/%m/%d %H:%M}\t{1}\t{2}".format(bp.date, bp.diastolic, bp.systolic))


if __name__ == "__main__":
    cmd()