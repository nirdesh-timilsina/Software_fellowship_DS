from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///test.db")

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
   return Session(engine)
