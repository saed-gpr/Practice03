# modules and global variables
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'sqlite:///./sqlite.db'


# create the engine
engine = create_engine(
    url = DATABASE_URL,
    connect_args={'check_same_thread' : False}
)

# create the SessionLocal
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# create the Base
Base = declarative_base()