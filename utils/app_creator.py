from flask import Flask

def create_app(name: str) -> Flask:
    app = Flask(name)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
    
    from tempfile import mkdtemp
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    
    from flask_session import Session
    Session(app)
    
    return app