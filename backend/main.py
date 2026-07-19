from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

app= FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Expense(BaseModel):
    category: str
    description: str= ""
    amount: float = Field(gt=0, description="Must be greater than 0")

class ExpenseOut(Expense):
    id: int

expenses: List[ExpenseOut] = []
next_id =1

@app.get("/")
def root():
    return{"message" : "Welcome to the Expense Tracker API!"}

@app.get("/expenses" , response_model= List[ExpenseOut])
async def get_expenses():
    return expenses

@app.post("/expenses", response_model=ExpenseOut)
async def add_expenses(expense: Expense):
    global next_id
    new_expense = ExpenseOut(id=str(next_id), **expense.model_dump())
    expenses.append(new_expense)
    next_id += 1
    return new_expense

@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int):
    for e in expenses:
        if e.id== expense_id:
            expenses.remove(e)
            return {"message": "deleted"}
        raise HTTPException(status_code= 404, detail="Expense not found")
















