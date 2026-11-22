# Personal Budget Manager
A small money diary used in the terminal. 

## Setup
Requires-python = ">=3.12" and [uv](https://docs.astral.sh/uv/).
```bash
cd budget-manager
uv sync
```

## Run
```bash
uv run budget-manager
```

Run it from inside the `budget-manager` folder: transactions are saved to `data/transactions.csv`.


## Example: adding a transaction
```text
$ uv run budget-manager

1) Add  2) List  3) Report  4) Save  q) Quit
Choose an option: 1
Date (YYYY-MM-DD): 2026-09-03
Kind (expense/income): expense
Category: food
Amount: 18.50
Added Transaction(T1, 2026-09-03, expense, food, 18.5, EUR)

Choose an option: 3
Income: 0.00
Expenses: 18.50
Balance: -18.50
  food: 18.50

Choose an option: 4
Saved.

Choose an option: q
```

If an input is invalid, the program explains why and goes back to the menu:

```text
Date (YYYY-MM-DD): 04/09/2026
error: date must be in ISO format, got 04/09/2026
```

## How the code is organised
Each file has one responsibility:

| File | Responsibility |
| --- | --- |
| `cli.py` | Interactive menu: reads user input and shows results. No calculations, no file access. |
| `validation.py` | Turns raw text into clean values (amount, date, kind, category) or raises a clear `ValueError`. Also checks CSV rows. |
| `models.py` | `Transaction` (refuses invalid data when created) and `Budget` (holds transactions, refuses duplicate IDs). |
| `services.py` | Business logic: balance, totals, totals per category, filters, sorting. Pure functions, no input or output. |
| `storage.py` | Saves to and loads from the CSV file. |
| `tests/test_budget.py` | Automatic tests for the rules above. |

## File contract

| | |
| --- | --- |
| Path | `data/transactions.csv` |
| Format | CSV with a header row |
| Encoding | UTF-8 |
| Columns | `id, date, kind, category, amount, currency` |
| Error policy | Invalid rows are skipped and reported with their row number (e.g. `Row 3: amount must be >0, got -5.0`); valid rows still load. |

Saving writes to a temporary file first and then replaces the real file, so a crash during saving can't leave a half-written file.

## Sample data

`data/sample_transactions.csv` contains valid rows and rows that break each rule on purpose. To try it:

```bash
cp data/sample_transactions.csv data/transactions.csv
uv run budget-manager
```
Note: this replaces `data/transactions.csv`; don't run it if you have real data you want to keep.


| Row | Problem | Expected |
| --- | --- | --- |
| 2–4, 10 | valid (row 10 has spaces and a capital) | loaded |
| 5 | negative amount | `warning: Row 5: amount must be >0, got -10.0`|
| 6 | date not in ISO format | `warning: Row 6: date must be in ISO format, got 04/09/2026`|
| 7 | unknown category | `warning: Row 7: category must be one of: ['food', 'medicines', 'rent', 'salary', 'transport'], got pizza` |
| 8 | missing amount | `warning: Row 8: missing amount`|
| 9 | duplicate id | `warning: Row 9: duplicate T3` |
| 11 | currency not 3 letters | `warning: Row 11: currency must be a 3 letter code, got EURO` |

## Tests
```bash
uv run pytest -v
```
Output:
```text
collected 3 items                                                                                                        

tests/test_budget.py::test_balance_of_one_income_two_expenses PASSED                                               [ 33%]
tests/test_budget.py::test_zero_amount_is_rejected PASSED                                                          [ 66%]
tests/test_budget.py::test_broken_row_is_reported_and_good_rows_load PASSED                                        [100%]

=================================================== 3 passed in 0.02s ====================================================
´´´

## Known limitations
- One wrong answer while adding cancels that transaction; the user starts again from the menu (no retries).
- Categories are a fixed list: rent, food, transport, salary, medicines.
- Dates must be written as `YYYY-MM-DD`.
- Amounts are stored in one currency (EUR by default); there is no currency conversion.
- Transactions can't be edited or deleted yet.
- The program must be run from the `budget-manager` folder (the data path is relative).