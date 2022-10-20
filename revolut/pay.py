from flask import (
    Blueprint,
    session,
    request,
    make_response,
)
from revolut.db import get_db
from sqlite3 import DatabaseError

bp = Blueprint("pay", __name__, url_prefix="/pay")

@bp.route("/", methods=("PUT",))
def pay():
    session_user_id = session.get("userid")
    if not session_user_id:
        return _make_error("", "You must be logged in to make a transaction", 401)
    
    username_from = request.form["from"]
    if not username_from.strip():
        return _make_error("", "Empty origin account username", 400)

    username_to = request.form["to"]
    if not username_to.strip():
        return _make_user_error("Empty target account username", 400)

    try:
        transaction_value = float(request.form["value"])
        if transaction_value < 0:
            return _make_pay_error("Transaction value must be a positive number", 400)
    except ValueError:
        return _make_pay_error("Transaction value is not a number", 400)

    db = get_db()

    user_from = _get_user(db, username_from)
    if not user_from:
        return _make_error("", f"Could not find origin user with username {username_from}", 404)
    if session_user_id != user_from["id"]:
        return _make_error("", "Origin account does not match the client ID", 401)

    user_to = _get_user(db, username_to)
    if not user_to:
        return _make_user_error(f"Could not find target user with username {username_to}", 404)

    user_from_balance = user_to["balance"] - transaction_value
    user_to_balance = user_to["balance"] + transaction_value
    if user_from_balance < 0:
        return _make_pay_error("Insufficient funds for this transaction", 403)

    try:
        db.execute(
            "INSERT INTO transactions (user_from,user_to,amount) VALUES (?,?,?)",
            (
                user_from["id"],
                user_to["id"],
                transaction_value,
            )
        )
        db.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (user_from_balance, user_from["id"])
        )
        db.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (user_to_balance, user_to["id"])
        )
        db.commit()
    except DatabaseError:
        return _make_error("", "Transaction could not be committed to the database", 500)

    return make_response("success", 200)


def _make_user_error(message: str, code: int):
    return _make_error("user", message, code)

def _make_pay_error(message: str, code: int):
    return _make_error("value", message, code)

def _make_error(reason: str, message: str, code: int):
    return make_response({ "reason": reason, "message": message }, code)


def _get_user(db, username: str):
    user = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchall()
    return user[0] if len(user) == 1 else None
