from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models.application import APPLICATION_STATUSES, Application

applications_bp = Blueprint("applications", __name__, url_prefix="/applications")


def can_view_application(application):
    return current_user.is_recruiting_staff or application.user_id == current_user.id


@applications_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "applicant":
        return redirect(url_for("index"))
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.created_at.desc()).all()
    return render_template("applications/dashboard.html", applications=applications)


@applications_bp.route("/<int:application_id>")
@login_required
def detail(application_id):
    application = Application.query.get_or_404(application_id)
    if not can_view_application(application):
        abort(403)
    return render_template("applications/detail.html", application=application, statuses=APPLICATION_STATUSES)


@applications_bp.route("/<int:application_id>/status", methods=["POST"])
@login_required
def update_status(application_id):
    if not current_user.is_recruiting_staff:
        abort(403)
    application = Application.query.get_or_404(application_id)
    status = request.form.get("status")
    if status not in APPLICATION_STATUSES:
        abort(400)
    application.status = status
    db.session.commit()
    flash("Application status updated.", "success")
    return redirect(url_for("applications.detail", application_id=application.id))
