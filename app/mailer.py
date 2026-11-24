"""
mailer.py – Email helper for StudyTrack.
Sends HTML reminder emails via SMTP (Gmail).
If SMTP is not configured, logs the email content to the console
so the app never crashes due to missing credentials.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def _get_smtp_config():
    """Read SMTP settings from environment variables."""
    return {
        "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", 587)),
        "username": os.getenv("SMTP_USERNAME", ""),
        "password": os.getenv("SMTP_PASSWORD", ""),
        "from_name": os.getenv("SMTP_FROM_NAME", "StudyTrack Reminders"),
    }


def is_smtp_configured():
    """Return True if SMTP username and password are set."""
    cfg = _get_smtp_config()
    return bool(cfg["username"] and cfg["password"])


def send_email(to_email, subject, html_body):
    """
    Send an HTML email. If SMTP is not configured, print the email
    content to the console (safe fallback for demos).
    Returns True on success, False on failure.
    """
    cfg = _get_smtp_config()

    # ----- Fallback: log to console -----
    if not cfg["username"] or not cfg["password"]:
        category = "NOTIFICATION"
        if "Lab Exam" in subject:
            category = "LAB EXAM"
        elif "Quiz" in subject:
            category = "QUIZ"
        elif "Mid-Sem" in subject:
            category = "MID-SEM"
        elif "Semester Exam" in subject:
            category = "SEMESTER EXAM"
        elif "Reminder:" in subject or "Assignment" in subject:
            category = "ASSIGNMENT"

        print("=" * 60)
        print(f"[MAILER] [{category}] SMTP not configured – logging email to console")
        print(f"  Category: {category}")
        print(f"  To:       {to_email}")
        print(f"  Subject:  {subject}")
        print("-" * 60)
        print(html_body[:500])
        if len(html_body) > 500:
            print("  ... (truncated)")
        print("=" * 60)
        return True  # Treat as "sent" so the notification_log records it

    # ----- Build the email -----
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{cfg['from_name']} <{cfg['username']}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    # ----- Send via SMTP -----
    try:
        with smtplib.SMTP(cfg["server"], cfg["port"]) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(cfg["username"], cfg["password"])
            server.sendmail(cfg["username"], to_email, msg.as_string())
        print(f"[MAILER] Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        print(f"[MAILER] Failed to send email to {to_email}: {e}")
        return False


def build_assignment_reminder_html(student_name, assignment):
    """Build a nicely formatted HTML email for an assignment reminder."""
    priority_colors = {"High": "#dc3545", "Medium": "#fd7e14", "Low": "#198754"}
    color = priority_colors.get(assignment["priority"], "#6c757d")

    return f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 24px; border-radius: 12px 12px 0 0;">
            <h1 style="color: white; margin: 0; font-size: 22px;">📚 StudyTrack Reminder</h1>
        </div>
        <div style="background: #ffffff; padding: 24px; border: 1px solid #e0e0e0;">
            <p style="font-size: 16px; color: #333;">Hi <strong>{student_name}</strong>,</p>
            <p style="font-size: 15px; color: #555;">
                Your assignment is due <strong style="color: #dc3545;">tomorrow</strong>!
            </p>
            <div style="background: #f8f9fa; border-left: 4px solid {color}; padding: 16px; margin: 16px 0; border-radius: 0 8px 8px 0;">
                <h3 style="margin: 0 0 8px; color: #333;">{assignment["title"]}</h3>
                <p style="margin: 4px 0; color: #666;"><strong>Subject:</strong> {assignment["subject"]}</p>
                <p style="margin: 4px 0; color: #666;"><strong>Due Date:</strong> {assignment["due_date"]}</p>
                <p style="margin: 4px 0;">
                    <strong>Priority:</strong>
                    <span style="background: {color}; color: white; padding: 2px 10px; border-radius: 12px; font-size: 13px;">
                        {assignment["priority"]}
                    </span>
                </p>
                <p style="margin: 4px 0; color: #666;"><strong>Status:</strong> {assignment["status"]}</p>
            </div>
            <p style="font-size: 14px; color: #888;">Don't forget to submit on time. Good luck! 🍀</p>
        </div>
        <div style="background: #f1f3f5; padding: 12px; text-align: center; border-radius: 0 0 12px 12px; border: 1px solid #e0e0e0; border-top: 0;">
            <p style="margin: 0; font-size: 12px; color: #aaa;">Sent by StudyTrack – Your Assignment & Exam Tracker</p>
        </div>
    </div>
    """


def build_exam_reminder_html(student_name, exam, days_left):
    """Build a nicely formatted HTML email for an exam reminder."""
    type_colors = {
        "Quiz": "#0d6efd",
        "Lab Exam": "#198754",
        "Mid-Sem": "#fd7e14",
        "Semester Exam": "#dc3545",
    }
    type_icons = {
        "Quiz": "📝",
        "Lab Exam": "🧪",
        "Mid-Sem": "📚",
        "Semester Exam": "🎓",
    }
    exam_type = exam.get("exam_type", "Exam")
    color = type_colors.get(exam_type, "#6c757d")
    icon = type_icons.get(exam_type, "📝")
    urgency = "tomorrow" if days_left <= 1 else f"in {days_left} days"

    return f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #f093fb, #f5576c); padding: 24px; border-radius: 12px 12px 0 0;">
            <h1 style="color: white; margin: 0; font-size: 22px;">{icon} {exam_type} Reminder</h1>
        </div>
        <div style="background: #ffffff; padding: 24px; border: 1px solid #e0e0e0;">
            <p style="font-size: 16px; color: #333;">Hi <strong>{student_name}</strong>,</p>
            <p style="font-size: 15px; color: #555;">
                Your <strong>{exam_type}</strong> is <strong style="color: #dc3545;">{urgency}</strong>!
            </p>
            <div style="background: #f8f9fa; border-left: 4px solid {color}; padding: 16px; margin: 16px 0; border-radius: 0 8px 8px 0;">
                <h3 style="margin: 0 0 8px; color: #333;">{exam["title"]}</h3>
                <p style="margin: 4px 0; color: #666;"><strong>Subject:</strong> {exam["subject"]}</p>
                <p style="margin: 4px 0;">
                    <strong>Type:</strong>
                    <span style="background: {color}; color: white; padding: 2px 10px; border-radius: 12px; font-size: 13px;">
                        {icon} {exam_type}
                    </span>
                </p>
                <p style="margin: 4px 0; color: #666;"><strong>Date:</strong> {exam["exam_date"]}</p>
                <p style="margin: 4px 0; color: #666;"><strong>Time:</strong> {exam.get("exam_time", "N/A")}</p>
                <p style="margin: 4px 0; color: #666;"><strong>Venue:</strong> {exam.get("venue", "N/A")}</p>
                <p style="margin: 4px 0; color: #666;"><strong>Syllabus:</strong> {exam.get("syllabus", "N/A")}</p>
            </div>
            <p style="font-size: 14px; color: #888;">Prepare well and stay confident! 💪</p>
        </div>
        <div style="background: #f1f3f5; padding: 12px; text-align: center; border-radius: 0 0 12px 12px; border: 1px solid #e0e0e0; border-top: 0;">
            <p style="margin: 0; font-size: 12px; color: #aaa;">Sent by StudyTrack – Your Assignment & Exam Tracker</p>
        </div>
    </div>
    """
