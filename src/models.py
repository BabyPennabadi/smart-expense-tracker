from datetime import date
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, PositiveFloat

class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1, example="Coffee")
    amount: PositiveFloat = Field(..., example=4.50)
    category: str = Field(..., min_length=1, example="Food")
    date: date = Field(..., example="2026-07-31")

class Expense(ExpenseCreate):
    id: str = Field(..., example="1a2b3c4d")

class CategorySummary(BaseModel):
    category: str
    total: float

class ExpenseSummary(BaseModel):
    overall_total: float
    by_category: Dict[str, float]
