from sqlite3 import Connection
from revolut.db import get_db

def _get_user(db: Connection, username: str):
    user = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchall()
    return user[0] if len(user) == 1 else None

def _make_error(reason, message):
    return { "reason": reason, "message": message }

def add(username_from: str, username_to: str, amount: float):
    db = get_db()
    user_from = _get_user(db, username_from)
    user_to = _get_user(db, username_to)

    if not user_from:
        return _make_error("", "User's account count not be fetched")

    if not user_to:
        return _make_error("user", "Recipient's account not found")
        
    if user_from["balance"] <= amount:
        return _make_error("value", "Insufficient funds")
    
    try:
        db.execute(
            "INSERT INTO transactions (user_from,user_to,amount) VALUES (?,?,?)",
            (
                user_from["id"],
                user_to["id"],
                amount,
            )
        )
        db.execute(
            "UPDATE users SET balance = balance - ? WHERE id = ?",
            (amount, user_from["id"])
        )
        db.execute(
            "UPDATE users SET balance = balance + ? WHERE id = ?",
            (amount, user_to["id"])
        )
        db.commit()
    except:
        return _make_error("", "Could not add transaction to the database")
