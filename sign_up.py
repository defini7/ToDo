from blueprint_common import *

from flask import render_template, flash

from werkzeug.security import generate_password_hash
from markupsafe import escape

b_sign_up = Blueprint("sign_up", __name__, static_folder="/static", template_folder="/templates")

@b_sign_up.route("/", methods=["GET", "POST"])
def sign_up():
    
    def flash_redirect(message):
        flash(message, "error")
        return render_template("sign_up.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        
        if not username:
            return flash_redirect("Missing username")
        
        user_data = get_db().execute(sql_text("SELECT * FROM users WHERE name = :name"), { "name": escape(username) }).fetchone()
        
        if user_data:
            return flash_redirect("Please choose another username")
        else:
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")
            
            if not password or not confirmation:
                return flash_redirect("Fill all fields") 
            
            if password != confirmation:
                return flash_redirect("Passwords don't match")
                
            hashed = generate_password_hash(password)
            
            get_db().execute(sql_text("INSERT INTO users (name, hash) VALUES(:name, :hash)"), { "name": escape(username), "hash": hashed })
            get_db().commit()
            
            return redirect(url_for("index"))
            
    else:
        return render_template("sign_up.html")
