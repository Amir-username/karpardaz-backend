from sqlmodel import create_engine, SQLModel, text

# DATABASE_URL = "sqlite:///./karpardaz.db"
DATABASE_URL = "postgresql://postgres.ptpccwwupnhylniobcha:nK55Di6p354Tk1@aws-0-eu-north-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def delete_jdetail_table():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS interview"))
        conn.commit()
