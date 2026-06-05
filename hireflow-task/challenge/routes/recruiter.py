from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models.application import Application
from models.interview import Interview
from models.job import Job
from models.user import User

recruiter_bp = Blueprint("recruiter", __name__)


@recruiter_bp.route("/recruiter/dashboard")
@login_required
def dashboard():
    if not current_user.is_recruiting_staff:
        abort(403)
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    applications = Application.query.order_by(Application.created_at.desc()).all()
    interviews = Interview.query.order_by(Interview.created_at.desc()).limit(8).all()
    return render_template("recruiter/dashboard.html", jobs=jobs, applications=applications, interviews=interviews)


@recruiter_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        abort(403)
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/dashboard.html", users=users)


@recruiter_bp.route("/admin/users/<int:user_id>/role", methods=["POST"])
@login_required
def update_user_role(user_id):
    if current_user.role != "admin":
        abort(403)
    user = User.query.get_or_404(user_id)
    role = request.form.get("role")
    if role not in {"applicant", "recruiter", "admin"}:
        abort(400)
    user.role = role
    db.session.commit()
    flash("User role updated.", "success")
    return redirect(url_for("recruiter.admin_dashboard"))
