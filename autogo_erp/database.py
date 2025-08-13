from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usaremos el SQLite que ya tienes en el repo: ./test.db
DATABASE_URL = "sqlite:///./test.db"

# Necesario para SQLite con SQLAlchemy en apps async/sync
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

