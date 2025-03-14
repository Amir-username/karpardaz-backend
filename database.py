from sqlmodel import create_engine, SQLModel

DATABASE_URL = "sqlite:///./karpardaz.db"
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)