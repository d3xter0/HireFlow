from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models.application import Application
from models.job import Job

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


def require_recruiter():
    if not current_user.is_authenticated or not current_user.is_recruiting_staff:
        abort(403)


@jobs_bp.route("/")
@login_required
def list_jobs():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return render_template("jobs/list.html", jobs=jobs)


@jobs_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_job():
    require_recruiter()
    if request.method == "POST":
        job = Job(
            title=request.form["title"].strip(),
            department=request.form["department"].strip(),
            location=request.form["location"].strip(),
            employment_type=request.form["employment_type"].strip(),
            description=request.form["description"].strip(),
            requirements=request.form["requirements"].strip(),
            recruiter_id=current_user.id,
        )
        db.session.add(job)
        db.session.commit()
        flash("Job published successfully.", "success")
        return redirect(url_for("recruiter.dashboard"))
    return render_template("jobs/form.html")


@jobs_bp.route("/<int:job_id>")
@login_required
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    existing_application = None
    if current_user.role == "applicant":
        existing_application = Application.query.filter_by(user_id=current_user.id, job_id=job.id).first()
    return render_template("jobs/detail.html", job=job, existing_application=existing_application)


@jobs_bp.route("/<int:job_id>/apply", methods=["GET", "POST"])
@login_required
def apply(job_id):
    if current_user.role != "applicant":
        abort(403)
    job = Job.query.get_or_404(job_id)
    if not job.is_active:
        abort(404)
    existing = Application.query.filter_by(user_id=current_user.id, job_id=job.id).first()
    if existing:
        flash("You have already applied for this job.", "info")
        return redirect(url_for("applications.detail", application_id=existing.id))
    if request.method == "POST":
        application = Application(
            user_id=current_user.id,
            job_id=job.id,
            cover_letter=request.form.get("cover_letter", "").strip(),
        )
        db.session.add(application)
        db.session.commit()
        flash("Application submitted. You can upload a resume from your application page.", "success")
        return redirect(url_for("applications.detail", application_id=application.id))
    return render_template("jobs/apply.html", job=job)
