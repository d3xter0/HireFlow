import os
from datetime import datetime, timedelta

from app import create_app, db
from models.application import Application
from models.interview import Interview
from models.job import Job
from models.resume import Resume
from models.user import User


PASSWORD = "Password123!"


def make_user(username, email, role):
    user = User(username=username, email=email, role=role)
    user.set_password(PASSWORD)
    return user


def write_resume(filename, candidate, role):
    resume_dir = os.path.join(os.path.dirname(__file__), "uploads", "resumes")
    os.makedirs(resume_dir, exist_ok=True)
    path = os.path.join(resume_dir, filename)
    content = (
        f"{candidate}\n"
        f"Target role: {role}\n\n"
        "Professional summary\n"
        "Experienced technology professional with strong delivery habits, clear communication, "
        "and a record of partnering with product and security teams.\n\n"
        "Selected experience\n"
        "- Led cross-functional initiatives from discovery through release.\n"
        "- Improved operational quality through automation, review discipline, and documentation.\n"
        "- Collaborated with recruiters and hiring panels in structured interview processes.\n"
    )
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    return path


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        alice = make_user("alice", "alice@example.com", "applicant")
        bob = make_user("bob", "bob@example.com", "applicant")
        recruiter = make_user("recruiter1", "recruiter1@example.com", "recruiter")
        admin = make_user("admin", "admin@example.com", "admin")
        db.session.add_all([alice, bob, recruiter, admin])
        db.session.flush()

        backend = Job(
            title="Backend Engineer",
            department="Platform Engineering",
            location="New York, NY",
            employment_type="Full-time",
            description=(
                "Build reliable APIs and data services for HireFlow's recruiting operations. "
                "You will work with product managers, designers, and infrastructure engineers "
                "to improve candidate pipelines and internal recruiter workflows."
            ),
            requirements=(
                "Python, Flask or Django experience, SQL data modeling, API design, automated testing, "
                "and comfort operating production services."
            ),
            recruiter_id=recruiter.id,
        )
        security = Job(
            title="Security Engineer",
            department="Trust and Security",
            location="Remote",
            employment_type="Full-time",
            description=(
                "Strengthen application security, review product changes, and build practical controls "
                "for a high-growth recruiting platform handling sensitive candidate data."
            ),
            requirements=(
                "Application security fundamentals, threat modeling, secure code review, cloud security, "
                "and clear written communication."
            ),
            recruiter_id=recruiter.id,
        )
        db.session.add_all([backend, security])
        db.session.flush()

        alice_app = Application(
            user_id=alice.id,
            job_id=backend.id,
            status="Interview Scheduled",
            cover_letter=(
                "I have spent the last four years building Python services for workflow-heavy teams. "
                "The Backend Engineer role is a strong match for my API and data modeling experience."
            ),
        )
        bob_app = Application(
            user_id=bob.id,
            job_id=security.id,
            status="Under Review",
            cover_letter=(
                "My background combines secure code review, incident response, and pragmatic risk communication. "
                "I would be excited to support HireFlow's trust and security roadmap."
            ),
        )
        db.session.add_all([alice_app, bob_app])
        db.session.flush()

        alice_resume_path = write_resume("alice_backend_resume.txt", "Alice Morgan", "Backend Engineer")
        bob_resume_path = write_resume("bob_security_resume.txt", "Bob Chen", "Security Engineer")
        db.session.add_all(
            [
                Resume(application_id=alice_app.id, filename="alice_backend_resume.txt", filepath=alice_resume_path),
                Resume(application_id=bob_app.id, filename="bob_security_resume.txt", filepath=bob_resume_path),
            ]
        )

        db.session.add_all(
            [
                Interview(
                    application_id=alice_app.id,
                    notes=(
                        "Strong systems thinking and clear ownership examples. Recommended for a technical panel "
                        "focused on API design and reliability tradeoffs."
                    ),
                    score=8,
                    recruiter_id=recruiter.id,
                    scheduled_at=datetime.utcnow() + timedelta(days=2),
                ),
                Interview(
                    application_id=bob_app.id,
                    notes=(
                        "Good security fundamentals and thoughtful communication. Follow up on cloud detection "
                        "experience in the next round."
                    ),
                    score=7,
                    recruiter_id=recruiter.id,
                    scheduled_at=datetime.utcnow() + timedelta(days=4),
                ),
            ]
        )
        db.session.commit()
        print("Seeded HireFlow database.")


if __name__ == "__main__":
    seed()
