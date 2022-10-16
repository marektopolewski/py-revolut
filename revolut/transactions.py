from sqlite3 import Connection
from revolut.db import get_db

def _get_user(db: Connection, username: str):
    user = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchall()
    if len(user) != 1:
        raise Exception("Invalid username: '{}'".format(username))
    return user[0]

def add(username_from: str, username_to: str, amount: float):
    db = get_db()

    user_from = _get_user(db, username_from)
    user_to = _get_user(db, username_to)
    
    print(user_from, user_to)

    if user_from["balance"] <= amount:
        raise Exception("Insufficient funds")
    
    try:
        db.execute(
            "INSERT INTO transactions (user_from,user_to,amount) VALUES (?,?,?)",
            (
                user_from["id"],
                user_to["id"],
                amount,
            )
        )
        db.commit()
    except Exception as e:
        raise Exception("Transaction failed, error: '{}'".format(e))
