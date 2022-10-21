from flask import (
    Blueprint,
    session,
    render_template,
    make_response,
    request
)
from revolut.db import get_db

bp = Blueprint("account", __name__, url_prefix="/account")

@bp.route("/", methods=("GET", "POST"))
def account():
    session_user_id = session.get("userid")
    if not session_user_id:
        return make_response("You must be logged in to access this page", 401)

    if request.method == "GET":
        return render_template("account/index.html")

    db = get_db()
    details = db.execute(
        "SELECT * FROM users WHERE id=?",
        (session_user_id,)
    ).fetchone()

    if not details:
        return make_response("Could not find the user in the database", 500)
    
    history = db.execute("""
            SELECT
                T.id, T.amount, T.created, T.pending,
                U.id, U.name, U.username,
                TRUE AS outgoing
            FROM transactions T
            JOIN users U ON T.user_to = U.id
            WHERE T.user_from = ?
        UNION
            SELECT
                T.id, T.amount, T.created, T.pending,
                U.id, U.name, U.username, 
                FALSE AS outgoing
            FROM transactions T
            JOIN users U ON T.user_from = U.id
            WHERE T.user_to = ?
        """, (session_user_id, session_user_id)
    ).fetchall()

    return make_response({
        "details": _row_to_dict(details),
        "history": _rows_to_dict(history)
    }, 200)

@bp.route("/transaction/<int:transaction_id>", methods=("GET", "POST"))
def get_transaction(transaction_id):
    session_user_id = session.get("userid")
    if not session_user_id:
        return make_response("You must be logged in to access this page", 401)

    if request.method == "GET":
        return render_template("account/transaction.html", id=transaction_id)
    
    db = get_db()
    transaction = db.execute(
        """
        SELECT *
        FROM transactions
        WHERE id=? AND (user_from=? OR user_to=?)
        """, (transaction_id, session_user_id, session_user_id)
    ).fetchone()

    if not transaction:
        return make_response("Could not find the transaction in the database", 500)

    user_from = db.execute(
        "SELECT username, name FROM users WHERE id=?", (transaction["user_from"],)
    ).fetchone()
    if not user_from:
        return make_response("Could not find the transaction in the database", 500)

    user_to = db.execute(
        "SELECT username, name FROM users WHERE id=?", (transaction["user_to"],)
    ).fetchone()
    if not user_to:
        return make_response("Could not find the transaction in the database", 500)
    
    return make_response({
        "transaction": _row_to_dict(transaction),
        "from": _row_to_dict(user_from),
        "to": _row_to_dict(user_to),
    }, 200)
    

from sqlite3 import Row
def _row_to_dict(row: Row):
    return { key: row[key] for key in row.keys() }

from typing import List
def _rows_to_dict(rows: List[Row]):
    return [_row_to_dict(row) for row in rows]
