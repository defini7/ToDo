from blueprint_common import *
from flask import flash, render_template

from werkzeug.security import check_password_hash
from markupsafe import escape

b_sign_in = Blueprint("sign_in", __name__, static_folder="/static", template_folder="/templates")

@b_sign_in.route("/", methods=["GET", "POST"])
def sign_in():
    
    def flash_redirect(message):
        flash(message, "error")
        return render_template("sign_in.html")
    
    session.clear()
    
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username:
            flash_redirect("Please, provide username")
        
        if not password:
            flash_redirect("Please, provide password")
            
        user_data = get_db().execute(sql_text("SELECT * FROM users WHERE name = :name"), { "name": escape(username) }).fetchone()
        if not user_data:
            return flash_redirect("Invalid username and/or password")
        
        id, _, hashed = user_data
        if not check_password_hash(hashed, password):
            return flash_redirect("Invalid password and/or password")
            
        session["user_id"] = id
        
        return redirect(url_for("index"))
    
    return render_template("sign_in.html")