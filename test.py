from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://test:asdfgh@192.168.100.49/test")
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
