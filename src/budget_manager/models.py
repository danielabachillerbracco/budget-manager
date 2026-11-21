import datetime
#constants
VALID_KINDS={"expense","income"}
VALID_CATEGORIES={"rent", "food", "transport", "salary", "medicines"}

#transactions class
class Transaction:
    def __init__(self, id:str, date:datetime.date, kind:str, category:str, amount:float, currency: str = "EUR"):
        #validation
        if not id:
            raise ValueError ("id must not be empty")
        if kind not in VALID_KINDS:
            raise ValueError(f"unknown kind, use one of {VALID_KINDS}")
        if category not in VALID_CATEGORIES:
            raise ValueError (f"category not allowed, use one of {VALID_CATEGORIES}")
        if amount<=0:
            raise ValueError (f"amount must be >0, got {amount}")
        if len(currency)!=3:
            raise ValueError(f"currency must be a 3 letter code, got {currency}")
        if not isinstance(date, datetime.date):
            raise ValueError(f"date must be a datetime.date, got {date!r}")
        self.id=id
        self.date=date
        self.kind=kind
        self.category=category
        self.amount=amount
        self.currency=currency
        
    @property 
    def signed_amount(self):
        if self.kind=="expense":
            return -self.amount
        else:
            return self.amount
        
    @classmethod
    def from_dict(cls, row:dict)->"Transaction":
        """Build a Transaction from a CSV row, where every value is text"""
        return cls(
            row["id"],
            datetime.date.fromisoformat(row["date"]),
            row["kind"],
            row["category"],
                float (row["amount"]),
            row["currency"]
            )
        
    def to_dict(self)->dict:
        """Return a transaction as a plain dict, ready to save"""
        return{
            "id":self.id,
            "date":self.date.isoformat(),
            "kind":self.kind,
            "category":self.category,
            "amount":self.amount,
            "currency":self.currency
            }
            
    def __repr__(self)->str:
        return f"Transaction({self.id}, {self.date}, {self.kind}, {self.category}, {self.amount}, {self.currency})"

class Budget:
    """Holds transactions and refuses a duplicate id"""
    def __init__(self)->None:
        self._transactions: list[Transaction]=[]
        
    def add(self, transaction: Transaction)->None:
        if any (t.id==transaction.id for t in self._transactions):
            raise ValueError(f"duplicate id {transaction.id}")
        self._transactions.append(transaction)
    
    def all(self)->list[Transaction]:
        return list(self._transactions)
        