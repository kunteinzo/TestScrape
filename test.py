from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from os import environ

engine = create_engine(f"mysql+pymysql://{environ['DBUR']}:{environ['DBPW']}@{environ['DBHT']}/{environ['DBDB']}")
meta = MetaData()

user = Table(
    "user", meta,
    Column("uid", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100))
)
meta.create_all(engine)

Session = sessionmaker(engine)

with Session() as ss:
    name = input("Name: ")
    print(ss.query(user).filter(user.c.name == name).all())
