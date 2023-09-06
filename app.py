from blueprint_common import *
from flask import render_template, request, session, redirect, flash

import os

from app_creator import create_app
from database import open_db, init_app
from helpers import login_required, handle_errors

from sqlalchemy import text as sql_text

from delete import b_delete
from sign_in import b_sign_in
from sign_up import b_sign_up
from sign_out import b_sign_out


app = create_app(__name__)

init_app(app)
open_db(os.getenv("DATABASE_URL"))

app.register_blueprint(b_delete, url_prefix="/delete")
app.register_blueprint(b_sign_in, url_prefix="/sign_in")
app.register_blueprint(b_sign_up, url_prefix="/sign_up")
app.register_blueprint(b_sign_out, url_prefix="/sign_out")
    

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    def flash_redirect(message):
        flash(message, "error")
        
        tasks = get_db().execute(sql_text("SELECT * FROM tasks WHERE user_id = :user_id"), { "user_id": session["user_id"] }).fetchall()  
        return render_template("index.html", tasks=tasks)
    
    if request.method == "POST":
        
        new_task = request.form.get("new_task")
        if not new_task: return flash_redirect("Please, specify a task")
        
        get_db().execute(sql_text("INSERT INTO tasks (user_id, task) VALUES (:user_id, :task)"),
                   { "user_id": session["user_id"], "task": new_task })
        
        get_db().commit()
        
        return redirect("/")
        
    else:
        tasks = get_db().execute(sql_text("SELECT * FROM tasks WHERE user_id = :user_id"), { "user_id": session["user_id"] }).fetchall()
        return render_template("index.html", tasks=tasks)


handle_errors(app)
