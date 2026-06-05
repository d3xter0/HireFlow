from datetime import datetime

from app import db


APPLICATION_STATUSES = (
    "Submitted",
    "Under Review",
    "Interview Scheduled",
    "Rejected",
    "Accepted",
)


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    status = db.Column(db.String(40), default="Submitted", nullable=False)
    cover_letter = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    applicant = db.relationship("User", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")
    resume = db.relationship("Resume", back_populates="application", uselist=False, cascade="all, delete-orphan")
    interviews = db.relationship("Interview", back_populates="application", lazy=True, cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint("user_id", "job_id", name="uq_user_job_application"),)
