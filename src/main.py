import uuid
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query, status

from src.models import Expense, ExpenseCreate, ExpenseSummary

app = FastAPI(
    title="Smart Expense Tracker API",
    description="REST API for managing personal expenses",
    version="1.0.0",
)

# In-memory storage for expenses
expenses_db: Dict[str, Expense] = {}


@app.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate):
    """Add a new expense."""
    expense_id = str(uuid.uuid4())[:8]
    expense = Expense(id=expense_id, **expense_in.model_dump())
    expenses_db[expense_id] = expense
    return expense


@app.get("/expenses", response_model=List[Expense])
def get_expenses(category: Optional[str] = Query(None, description="Filter by category")):
    """View all expenses, with optional filtering by category."""
    if category:
        return [e for e in expenses_db.values() if e.category.lower() == category.lower()]
    return list(expenses_db.values())


@app.get("/expenses/summary", response_model=ExpenseSummary)
def get_expense_summary():
    """Calculate total expenses overall and grouped by category."""
    overall = sum(e.amount for e in expenses_db.values())
    by_cat: Dict[str, float] = {}

    for e in expenses_db.values():
        by_cat[e.category] = round(by_cat.get(e.category, 0.0) + e.amount, 2)

    return ExpenseSummary(
        overall_total=round(overall, 2),
        by_category=by_cat
    )


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: str):
    """Delete an expense by ID."""
    if expense_id not in expenses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID '{expense_id}' not found."
        )
    del expenses_db[expense_id]
    return None
