import datetime
from budget_manager.models import VALID_CATEGORIES, VALID_KINDS

REQUIRED = ["id", "date", "kind", "category", "amount", "currency"]

def parse_amount(text: str) -> float:
    """Turn text like '18.50' to 18.5
    Raises ValueError: if text is not a number or amount is not > 0"""
    try:
        amount=float(text.strip())
    except ValueError:
        raise ValueError(f"amount must be a number, got {text}")
    if amount<=0:
        raise ValueError(f"amount must be >0, got {amount}")
    return amount

def parse_date(text: str) -> datetime.date:
    """Turn text like '2026-09-04' to date object 
    Raises ValueError: if date not in ISO format YYYY-MM-DD"""
    try:
        date=datetime.date.fromisoformat(text.strip())
    except ValueError:
        raise ValueError(f"date must be in ISO format, got {text}")
    return date
    
def parse_kind(text: str) -> str:
    """Turn text like ' Expense' to 'expense'
    Raises ValueError: if kind not in VALID_KINDS"""
    kind= text.strip().lower()
    if kind not in VALID_KINDS:
        raise ValueError(f"kind must be one of: {sorted(VALID_KINDS)}, got {text}")
    return kind

def parse_category(text:str)->str:
    """Turn text like ' Food' to 'food'
    Raises ValueError: if category not in VALID_CATEGORIES"""
    category= text.strip().lower()
    if category not in VALID_CATEGORIES:
        raise ValueError(f"category must be one of: {sorted(VALID_CATEGORIES)}, got {text}")    
    return category
        
def validate_row(row:dict, line:int, seen_ids: set[str])-> list[str]:
    """Return the error messages for one CSV row; an empty list means valid"""
    missing = [f for f in REQUIRED if not (row.get(f) or "").strip()]
    if missing:
        return[f"Row {line}: missing {', '.join(missing)}"]
    errors=[]
    
    try:
        parse_amount(row["amount"])
    except ValueError as e:
        errors.append(f"Row {line}: {e}")
    try:
        parse_date(row["date"])
    except ValueError as e:
        errors.append(f"Row {line}: {e}")
    try:
        parse_kind(row["kind"])
    except ValueError as e:
        errors.append(f"Row {line}: {e}")
    try:
        parse_category(row["category"])
    except ValueError as e:
        errors.append(f"Row {line}: {e}")
    
    if row["id"].strip() in seen_ids:
        errors.append(f"Row {line}: duplicate {row["id"]}")
    return errors
