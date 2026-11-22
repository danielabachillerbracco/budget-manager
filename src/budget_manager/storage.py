import csv
from pathlib import Path

from budget_manager.models import Transaction
from budget_manager.validation import REQUIRED, validate_row

DATA_DIR = Path("data")
DEFAULT_FILE= DATA_DIR/"transactions.csv"

def load(path: Path) -> tuple [list[Transaction], list[str]]:
    """Read transactions from a CSV file.
    Returns: 
    transactions, error message for rejected rows"""
    if not path.exists():
        return [], []
    transactions: list[Transaction]=[] 
    errors: list[str] = []
    seen_ids: set[str]= set()
    with path.open("r", encoding="utf-8", newline="") as f:
        for line, row in enumerate(csv.DictReader(f), start=2): #line 1 is the header
            row_errors = validate_row(row,line, seen_ids)
            if row_errors:
                errors.extend(row_errors)
                continue
            try:
                transaction = Transaction.from_dict(row)
            except ValueError as e:
                errors.append(f"Row {line}: {e}")
                continue
            transactions.append(transaction)
            seen_ids.add(row["id"].strip())
    return transactions, errors

def save(transactions: list[Transaction], path: Path)-> None:
    """Write all transactions to the CSV safely (temp file then replace)"""
    path.parent.mkdir(exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer= csv.DictWriter(f, fieldnames=REQUIRED)
        writer.writeheader()
        for t in transactions:
            writer.writerow(t.to_dict())
    tmp.replace(path)
            