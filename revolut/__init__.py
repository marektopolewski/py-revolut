import os
from flask import (
    Flask,
    render_template,
    request,
    make_response,
    redirect,
    url_for,
    session,
)
from revolut.transactions import add
from revolut.db import with_db
from revolut.auth import bp as AuthBlueprint

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ledger.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with_db(app)

    @app.get("/")
    def index():
        if not session.get("userid"):
            return redirect(url_for("auth.login"))
        return render_template("./index.html")

    @app.post("/api/transaction")
    def add_transaction():
        try:
            t_from = request.form['from']
            t_to = request.form['to']
            t_value = float(request.form['value'])
            if not t_from.strip() or not t_from.strip() or t_value == 0:
                raise Exception("Invalid form arguments")
            add(t_from, t_to, t_value)
        except Exception as e:
            return make_response(str(e), 400)

        return redirect(url_for("index"))
    
    app.register_blueprint(AuthBlueprint)
    
    return app
