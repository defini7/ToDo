from .common import *
from flask import render_template, flash

class IndexView(views.MethodView):
    @login_required
    def get(self):
        tasks = get_db().execute(sql_text("SELECT * FROM tasks WHERE user_id = :user_id"), { "user_id": session["user_id"] }).fetchall()
        return render_template("index.html", tasks=tasks)
    
    @login_required
    def post(self):
        def flash_redirect(message):
            flash(message, "error")
            return self.get()
        
        new_task = request.form.get("new_task")
        if not new_task: return flash_redirect("Please, specify a task")
        
        get_db().execute(sql_text("INSERT INTO tasks (user_id, task) VALUES (:user_id, :task)"),
                   { "user_id": session["user_id"], "task": new_task })
        
        get_db().commit()
        
        return redirect("/")
    