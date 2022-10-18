from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
)
from werkzeug.security import check_password_hash, generate_password_hash
from revolut.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/checkusername", methods=("POST",))
def checkUsername():
    username = request.get_json()["username"]

    db = get_db()
    users = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchall()
    
    return { "valid": len(users) == 0 }

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    fname = request.form["fname"].strip()
    lname = request.form["lname"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()
    username = request.form["username"].strip()

    if not fname or not lname or not email or not username:
        return make_response("Missing user data for registration", 400)

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (name,username,email,password) VALUES (?,?,?,?)",
            (
                fname + " " + lname,
                username,
                email,
                generate_password_hash(password)
            ),
        )
        db.commit()
    except:
        return make_response("Could not add the user to the database", 500)
    
    return redirect(url_for("auth.login"))

@bp.route("/login", methods=("GET", "POST"))
def login():    
    if request.method == "GET":
        if session.get("userid"):
            return redirect(url_for("index"))
        return render_template("auth/login.html")
    
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    if not username or not password:
        return make_response("Missing user data for login", 400)

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()
    
    if not user or not check_password_hash(user["password"], password):
        return make_response("Login failed", 400)
    
    session.clear()
    session["userid"] = user["id"]
    session["username"] = user["username"]

    return make_response("success", 200)

@bp.route("/logout", methods=("GET", "POST"))
def logout():
    session.clear()
    if request.method == "GET":
        return redirect(url_for("auth.login"))
    return make_response("success", 200)
