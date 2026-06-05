from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models.application import Application
from models.interview import Interview

interviews_bp = Blueprint("interviews", __name__, url_prefix="/interviews")


@interviews_bp.route("/application/<int:application_id>/new", methods=["GET", "POST"])
@login_required
def create(application_id):
    if not current_user.is_recruiting_staff:
        abort(403)
    application = Application.query.get_or_404(application_id)
    if request.method == "POST":
        scheduled_at = request.form.get("scheduled_at")
        interview = Interview(
            application_id=application.id,
            notes=request.form["notes"].strip(),
            score=int(request.form["score"]),
            recruiter_id=current_user.id,
            scheduled_at=datetime.fromisoformat(scheduled_at) if scheduled_at else None,
        )
        db.session.add(interview)
        application.status = "Interview Scheduled"
        db.session.commit()
        flash("Interview notes saved.", "success")
        return redirect(url_for("applications.detail", application_id=application.id))
    return render_template("interviews/form.html", application=application)


@interviews_bp.route("/")
@login_required
def list_interviews():
    if not current_user.is_recruiting_staff:
        abort(403)
    interviews = Interview.query.order_by(Interview.created_at.desc()).all()
    return render_template("interviews/list.html", interviews=interviews)
