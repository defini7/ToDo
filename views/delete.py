from .common import *

class DeleteView(views.MethodView):
    
    @login_required
    def post(self):
        tasks_ids = request.get_json()
        for id in tasks_ids:
            get_db().execute(sql_text("DELETE FROM tasks WHERE id = :id AND user_id = :user_id"),
                        { "id": id, "user_id": session["user_id"] })
        
        get_db().commit()
        return redirect(url_for("index"))
