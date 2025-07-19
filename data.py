from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Double
from sqlalchemy.orm import sessionmaker

engine = create_engine("mariadb+pymysql://test:asdfgh@127.0.0.1/test")
meta = MetaData()

movie = Table(
    "Movie", meta,
    Column("id", String(50), primary_key=True),
    Column("titleEn", String(200)),
    Column("titleMm", String(200)),
    Column("type", String(10)),
    Column("rating", Double()),
    Column("duration", String(10)),
    Column("sizeFullHd", Integer),
    Column("sizeHd", Integer),
    Column("sizeSd", Integer),
    Column("contentId", String(50)),
    Column("publishDate", String(20)),

)

meta.create_all(engine)

Session = sessionmaker(engine)