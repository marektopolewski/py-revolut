from flask import (
    Blueprint,
    session,
    render_template,
    make_response,
)
from revolut.db import get_db

bp = Blueprint("account", __name__, url_prefix="/account")

@bp.route("/", methods=("GET",))
def account():
    if not session.get("userid"):
        return make_response("You must be logged in to access this page", 401)
    return render_template("account/index.html")

@bp.route("/fetch", methods=("GET", "POST"))
def get_user_and_transactions():
    session_user_id = session.get("userid")
    if not session_user_id:
        return make_response("You must be logged in to access this page", 401)

    db = get_db()
    details = db.execute(
        "SELECT * FROM users WHERE id=?",
        (session_user_id,)
    ).fetchone()
    
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


from sqlite3 import Row
def _row_to_dict(row: Row):
    return { key: row[key] for key in row.keys() }

from typing import List
def _rows_to_dict(rows: List[Row]):
    return [_row_to_dict(row) for row in rows]
