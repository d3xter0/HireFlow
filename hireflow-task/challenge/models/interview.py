from datetime import datetime

from app import db


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    recruiter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    scheduled_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    application = db.relationship("Application", back_populates="interviews")
    recruiter = db.relationship("User", back_populates="interviews")
