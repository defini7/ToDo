from blueprint_common import *

b_sign_out = Blueprint("sign_out", __name__, static_folder="/static", template_folder="/templates")

@b_sign_out.route("/")
@login_required
def sign_out():
    session.clear()
    return redirect(url_for("index"))
