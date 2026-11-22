import pytest
import datetime

from budget_manager.models import Transaction
from budget_manager.services import balance
from budget_manager.storage import load

#Normal case
def test_balance_of_one_income_two_expenses():
    transactions = [
        Transaction("T1", datetime.date(2026, 9, 1), "income", "salary", 100),
        Transaction("T2", datetime.date(2026, 9, 2), "expense", "food", 40),
        Transaction("T3", datetime.date(2026, 9, 3), "expense", "transport", 20),
    ]
    assert balance(transactions) == 40

#Boundary: a zero or negative amount must be refused
def test_zero_amount_is_rejected():
    with pytest.raises(ValueError, match="amount must be >0"):
        Transaction("T100", datetime.date(2026, 2, 1), "income", "salary", 0)
      
#Boundary: CSV with a broken row loads the good rows and reports the bad ones with row number
def test_broken_row_is_reported_and_good_rows_load(tmp_path):
    path = tmp_path / "transactions.csv"
    path.write_text(
        "id,date,kind,category,amount,currency\n"
        "T1,2026-09-01,income,salary,1000,EUR\n"
        "T2,2026-09-03,expense,food,-5,EUR\n"
        "T3,2026-09-04,expense,transport,40,EUR\n",
        encoding="utf-8",
    )
    transactions, errors = load(path)
    assert [t.id for t in transactions] == ["T1", "T3"]
    assert len(errors) == 1
    assert errors[0].startswith("Row 3:")
    assert "amount" in errors[0]

