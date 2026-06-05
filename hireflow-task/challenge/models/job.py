from datetime import datetime

from app import db


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    employment_type = db.Column(db.String(50), nullable=False, default="Full-time")
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    recruiter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    recruiter = db.relationship("User", back_populates="jobs")
    applications = db.relationship("Application", back_populates="job", lazy=True)
