import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

if not os.getenv("DB_PASSWORD"):
    raise RuntimeError("Falta configurar DB_PASSWORD")

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "13749")),
    database=os.getenv("DB_NAME"),
    query={"charset": "utf8mb4"}
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {}},
    pool_pre_ping=True
)

connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
Base.metadata.bind = engine
