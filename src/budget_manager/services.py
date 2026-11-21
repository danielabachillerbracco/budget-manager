from budget_manager.models import Transaction

def balance(transactions: list[Transaction]) -> float:
    """Return the total balance (income minus expenses)"""
    return sum(t.signed_amount for t in transactions)

def total_by_category(transactions: list[Transaction]) -> dict[str, float]:
    """Return expenses and income by category"""
    totals: dict[str, float] = {}
    for t in transactions:
        if t.kind=="expense":
            totals[t.category] = totals.get(t.category, 0) + t.amount 
    return totals

def filter_by_kind(transactions: list[Transaction], kind:str) -> list[Transaction]:
    """Return only the transactions of one kind in their original order"""
    return [t for t in transactions if t.kind ==kind]

def filter_by_month(transactions: list[Transaction], month:int) -> list[Transaction]:
    """Return only the transactions of one date in their original order"""
    return [t for t in transactions if t.date.month == month]

def sorted_by_date (transactions: list[Transaction]) -> list[Transaction]:
    """Return transactions by date"""
    return sorted(transactions, key=lambda t: t.date)

def total_income(transactions: list[Transaction]) -> float:
    """Return the total income"""
    return sum(t.amount for t in transactions if t.kind=="income" )

def total_expense(transactions: list[Transaction]) -> float:
    """Return the total expense"""
    return sum(t.amount for t in transactions if t.kind=="expense" )

def summary (transactions: list[Transaction])-> dict[str, float]:
    return{
        "income": total_income(transactions),
        "expenses": total_expense(transactions),
        "balance": balance(transactions)
    }






