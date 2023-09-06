from flask import render_template, session, redirect, url_for
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from functools import wraps

def apology(message, code=400):
    return render_template("apology.html", top=code, bottom=message)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("sign_in.sign_in"))
        return f(*args, **kwargs)

    return decorated_function

def handle_errors(app):
    def errorhandler(e):
        if not isinstance(e, HTTPException):
            e = InternalServerError()
        return apology(e.name, e.code)

    for code in default_exceptions:
        app.errorhandler(code)(errorhandler)
