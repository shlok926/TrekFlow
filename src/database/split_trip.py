# src/database/split_trip.py
from src.database.db import get_connection

def add_expense(trip_id: int, description: str, amount: float, paid_by: str, split_between_list: list) -> bool:
    """
    Saves a new group expense to the database.
    split_between_list is a list of group member names (e.g. ['Amit', 'Rahul', 'Sumit'])
    """
    split_between_str = ",".join(split_between_list)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO expenses (trip_id, description, amount, paid_by, split_between) VALUES (?, ?, ?, ?, ?)",
            (trip_id, description, amount, paid_by, split_between_str)
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_expenses(trip_id: int) -> list:
    """
    Retrieves all expenses logged under a specific trip.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, description, amount, paid_by, split_between, created_at FROM expenses WHERE trip_id=? ORDER BY created_at DESC",
            (trip_id,)
        )
        rows = cursor.fetchall()
        expenses = []
        for r in rows:
            expenses.append({
                "id": r[0],
                "description": r[1],
                "amount": r[2],
                "paid_by": r[3],
                "split_between": r[4].split(","),
                "created_at": r[5]
            })
        return expenses
    finally:
        conn.close()

def delete_expense(trip_id: int, expense_id: int) -> bool:
    """
    Deletes a logged expense.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM expenses WHERE trip_id=? AND id=?", (trip_id, expense_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()

def calculate_settlements(trip_id: int) -> dict:
    """
    Calculates net balances and the greedy minimum payments to settle all group debts.
    Returns:
      {
        "balances": {"MemberA": 1000.0, "MemberB": -600.0, ...},
        "settlements": [{"from": "MemberB", "to": "MemberA", "amount": 600.0}, ...]
      }
    """
    expenses = get_expenses(trip_id)
    balances = {}
    
    # Calculate net balances
    for exp in expenses:
        paid_by = exp["paid_by"]
        amount = exp["amount"]
        split_between = exp["split_between"]
        
        if not split_between:
            continue
            
        share = amount / len(split_between)
        
        # Credit the payer
        balances[paid_by] = balances.get(paid_by, 0.0) + amount
        
        # Debit the split members
        for member in split_between:
            balances[member] = balances.get(member, 0.0) - share
            
    # Clean up very small rounding errors
    balances = {name: round(bal, 2) for name, bal in balances.items() if abs(bal) > 0.01}
    
    # Greedy Settlement Matching
    creditors = []
    debtors = []
    
    for name, bal in balances.items():
        if bal > 0:
            creditors.append([name, bal])
        elif bal < 0:
            debtors.append([name, -bal]) # store debt as positive
            
    settlements = []
    
    while creditors and debtors:
        # Sort to greedily match largest creditor and debtor
        creditors.sort(key=lambda x: x[1], reverse=True)
        debtors.sort(key=lambda x: x[1], reverse=True)
        
        debtor_name, debt = debtors[0]
        creditor_name, credit = creditors[0]
        
        settle_amt = round(min(debt, credit), 2)
        if settle_amt > 0.01:
            settlements.append({
                "from": debtor_name,
                "to": creditor_name,
                "amount": settle_amt
            })
            
        # Update remaining amounts
        debtors[0][1] -= settle_amt
        creditors[0][1] -= settle_amt
        
        # Pop empty balances
        if debtors[0][1] < 0.01:
            debtors.pop(0)
        if creditors[0][1] < 0.01:
            creditors.pop(0)
            
    return {
        "balances": balances,
        "settlements": settlements
    }
