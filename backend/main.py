from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import SQLModel, select, Field
from db import create_db_and_table, get_session
from typing import List

app= FastAPI(title="Expense Tracker API")

@app.on_event("startup")
async def startup_event():
    create_db_and_table()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# class Expense(BaseModel):
#     category: str
#     description: str= ""
#     amount: float = Field(gt=0, description="Must be greater than 0")

class Expense(SQLModel, table=True):
    id: int = Field(primary_key=True)
    category: str
    description: str= ""
    amount: float = Field(gt=0, description="Must be greater than 0")

class ExpenseIn(BaseModel):
    category: str
    description: str= ""
    amount: float = Field(gt=0, description="Must be greater than 0")

class ExpenseOut(BaseModel):
    id: int 
    category: str
    description: str= ""
    amount: float = Field(gt=0, description="Must be greater than 0")

class User(SQLModel, table=True):
    id: int= Field(primary_key=True)
    username: str
    email: str
    password: str

class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

@app.get("/")
def root():
    return{"message" : "Welcome to the Expense Tracker API!"}

@app.get("/expenses" , response_model= List[ExpenseOut])
async def get_expenses():
    session= next(get_session())
    expenses = session.exec(select(Expense)).all()
    return expenses

@app.post("/expenses", response_model=ExpenseOut)
async def add_expenses(expenseIn: ExpenseIn):

    expense = Expense.model_validate(expenseIn)

    session= next(get_session())
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense

@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int):
    session= next(get_session())
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    session.delete(expense)
    session.commit()
    return {"message": "Expense deleted"}

@app.post("/users", response_model=UserOut)
async def add_user(userIn: UserIn):
    user = User.model_validate(userIn)

    session= next(get_session())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
















