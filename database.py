from sqlmodel import create_engine

DATABASE_URL = "sqlite:///./karpardaz.db"
engine = create_engine(DATABASE_URL, echo=True)