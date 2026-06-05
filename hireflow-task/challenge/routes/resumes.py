import os
from uuid import uuid4

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from models.application import Application
from models.resume import Resume

resumes_bp = Blueprint("resumes", __name__, url_prefix="/resumes")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_RESUME_EXTENSIONS"]


def can_access_resume(resume):
    return current_user.is_recruiting_staff or resume.application.user_id == current_user.id


@resumes_bp.route("/<int:application_id>/upload", methods=["GET", "POST"])
@login_required
def upload(application_id):
    application = Application.query.get_or_404(application_id)
    if application.user_id != current_user.id:
        abort(403)
    if request.method == "POST":
        file = request.files.get("resume")
        if not file or file.filename == "":
            flash("Please choose a resume file.", "danger")
            return render_template("resumes/upload.html", application=application)
        if not allowed_file(file.filename):
            flash("Accepted formats are PDF, DOC, DOCX, and TXT.", "danger")
            return render_template("resumes/upload.html", application=application)

        original_name = secure_filename(file.filename)
        stored_name = f"{uuid4().hex}_{original_name}"
        resume_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "resumes")
        os.makedirs(resume_dir, exist_ok=True)
        filepath = os.path.join(resume_dir, stored_name)
        file.save(filepath)

        if application.resume:
            application.resume.filename = original_name
            application.resume.filepath = filepath
        else:
            db.session.add(Resume(application_id=application.id, filename=original_name, filepath=filepath))
        db.session.commit()
        flash("Resume uploaded.", "success")
        return redirect(url_for("applications.detail", application_id=application.id))
    return render_template("resumes/upload.html", application=application)


@resumes_bp.route("/<int:resume_id>/download")
@login_required
def download(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if not os.path.exists(resume.filepath):
        abort(404)
    return send_file(resume.filepath, as_attachment=True, download_name=resume.filename)
