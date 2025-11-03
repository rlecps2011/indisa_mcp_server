import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Example DSN for Azure SQL:
# mssql+pyodbc://<user>:<password>@<server>:1433/<database>?driver=ODBC+Driver+18+for+SQL+Server
# Please fill .env variables or replace values below.
DB_USER = os.getenv("DB_USER", "your_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_SERVER = os.getenv("DB_SERVER", "yourserver.database.windows.net")
DB_NAME = os.getenv("DB_NAME", "your_database")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

CONNECTION_STRING = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:1433/{DB_NAME}?driver={DB_DRIVER.replace(' ', '+')}"
)

# For local testing without real Azure SQL, you can set SQLITE_URL to use SQLite:
SQLITE_URL = os.getenv("SQLITE_URL", None)

engine = create_engine(SQLITE_URL if SQLITE_URL else CONNECTION_STRING, fast_executemany=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    """Yields a SQLAlchemy session. Use as: with get_db_session() as session:"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
