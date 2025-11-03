from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    cidade = Column(String(100), nullable=True)
    email = Column(String(200), nullable=True)

# Helper: create tables (only for development / SQLite testing)
def create_tables(engine):
    Base.metadata.create_all(bind=engine)
