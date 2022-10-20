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
from revolut.db import with_db
from revolut.auth import bp as AuthBlueprint
from revolut.pay import bp as PayBlueprint
from revolut.account import bp as AccountBlueprint

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

    @app.get("/")
    def index():
        if not session.get("userid"):
            return redirect(url_for("auth.login"))
        return render_template("index.html", username=session.get("username"))

    with_db(app)
    app.register_blueprint(AuthBlueprint)
    app.register_blueprint(PayBlueprint)
    app.register_blueprint(AccountBlueprint)
    
    return app
