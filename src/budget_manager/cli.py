import sys

from budget_manager.models import Budget, Transaction
from budget_manager.services import sorted_by_date, summary, total_by_category
from budget_manager.storage import DEFAULT_FILE, load, save
from budget_manager.validation import parse_amount, parse_category, parse_date, parse_kind


def add_transaction(budget: Budget) -> None:
    """Ask the user for a new transaction and add it to the budget."""
    new_id = f"T{len(budget.all()) + 1}"
    try:
        date = parse_date(input("Date (YYYY-MM-DD): "))
        kind = parse_kind(input("Kind (expense/income): "))
        category = parse_category(input("Category: "))
        amount = parse_amount(input("Amount: "))
        transaction = Transaction(new_id, date, kind, category, amount)
        budget.add(transaction)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return
    print(f"Added {transaction}")


def show_list(budget: Budget) -> None:
    """Print all transactions, sorted by date."""
    for transaction in sorted_by_date(budget.all()):
        print(transaction)


def show_report(budget: Budget) -> None:
    """Print income, expenses, balance and expenses per category."""
    totals = summary(budget.all())
    print(f"Income: {totals['income']:.2f}")
    print(f"Expenses: {totals['expenses']:.2f}")
    print(f"Balance: {totals['balance']:.2f}")
    for category, total in total_by_category(budget.all()).items():
        print(f"  {category}: {total:.2f}")


def main() -> int:
    """Run the interactive menu."""
    transactions, errors = load(DEFAULT_FILE)
    for message in errors:
        print(f"warning: {message}", file=sys.stderr)
    budget = Budget()
    for transaction in transactions:
        budget.add(transaction)

    while True:
        print("\n1) Add  2) List  3) Report  4) Save  q) Quit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_transaction(budget)
        elif choice == "2":
            show_list(budget)
        elif choice == "3":
            show_report(budget)
        elif choice == "4":
            save(budget.all(), DEFAULT_FILE)
            print("Saved.")
        elif choice == "q":
            break
        else:
            print("Unknown option, try again.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())