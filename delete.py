from blueprint_common import *

b_delete = Blueprint("delete", __name__, static_folder="/static", template_folder="/templates")

@b_delete.route("/", methods=["POST"])
@login_required
def delete():
    tasks_ids = request.get_json()
    for id in tasks_ids:
       get_db().execute(sql_text("DELETE FROM tasks WHERE id = :id AND user_id = :user_id"),
                   { "id": id, "user_id": session["user_id"] })
        
    get_db().commit()
    
    return redirect(url_for("index"))
