from .common import *

class SignOutView(views.MethodView):
    
    def get(self):
        session.clear()
        return redirect(url_for("index"))
