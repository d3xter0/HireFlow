import os
import sys

from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy

from config import Config

sys.modules.setdefault("app", sys.modules[__name__])

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "resumes"), exist_ok=True)

    from models.user import User
    from routes.auth import auth_bp
    from routes.jobs import jobs_bp
    from routes.applications import applications_bp
    from routes.resumes import resumes_bp
    from routes.interviews import interviews_bp
    from routes.recruiter import recruiter_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(resumes_bp)
    app.register_blueprint(interviews_bp)
    app.register_blueprint(recruiter_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            if current_user.role == "applicant":
                return redirect(url_for("applications.dashboard"))
            if current_user.role == "recruiter":
                return redirect(url_for("recruiter.dashboard"))
            if current_user.role == "admin":
                return redirect(url_for("recruiter.admin_dashboard"))
        return render_template("index.html")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
