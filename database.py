from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///menu.db", echo=True)

class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)










