from os import getenv

from utils.app_creator import create_app
from utils.database import open_db, init_app
from utils.helpers import handle_errors, add_urls

from views.index import IndexView
from views.delete import DeleteView
from views.sign_in import SignInView
from views.sign_up import SignUpView
from views.sign_out import SignOutView


app = create_app(__name__)

init_app(app)
open_db(getenv("DATABASE_URL"))

add_urls(app, [
    ("/", IndexView, "index"),
    ("/delete", DeleteView, "delete"),
    ("/sign_in", SignInView, "sign_in"),
    ("/sign_up", SignUpView, "sign_up"),
    ("/sign_out", SignOutView, "sign_out")
])

handle_errors(app)
