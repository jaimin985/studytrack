"""
scheduler.py – APScheduler-based reminder engine for StudyTrack.
Checks for upcoming assignment deadlines and exams, then sends
email reminders (or logs them if SMTP is not configured).
A notification_log table prevents duplicate sends.
"""

import os
from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from db import get_connection, execute_query
from mailer import send_email, build_assignment_reminder_html, build_exam_reminder_html


def _already_notified(user_id, item_type, item_id, days_before):
    """Check if we already sent this specific reminder."""
    rows = execute_query(
        "SELECT id FROM notification_log "
        "WHERE user_id=%s AND item_type=%s AND item_id=%s AND days_before=%s",
        (user_id, item_type, item_id, days_before),
        fetch=True,
    )
    return len(rows) > 0


def _log_notification(user_id, item_type, item_id, days_before):
    """Record that we sent a reminder so we don't send it again."""
    execute_query(
        "INSERT IGNORE INTO notification_log (user_id, item_type, item_id, days_before) "
        "VALUES (%s, %s, %s, %s)",
        (user_id, item_type, item_id, days_before),
        commit=True,
    )


def run_reminder_check():
    """
    Core reminder logic – called by the scheduler or manually.
    - Assignments: remind 1 day before due date (if not completed).
    - Exams: remind 3 days and 1 day before exam date.
    """
    print("[SCHEDULER] Running reminder check...")
    today = date.today()
    tomorrow = today + timedelta(days=1)
    three_days = today + timedelta(days=3)

    # ---- Assignment reminders (1 day before) ----
    assignments = execute_query(
        "SELECT a.*, u.name AS student_name, u.email AS student_email "
        "FROM assignments a JOIN users u ON a.user_id = u.id "
        "WHERE a.due_date = %s AND a.status != 'Completed'",
        (tomorrow,),
        fetch=True,
    )
    for a in assignments:
        if not _already_notified(a["user_id"], "assignment", a["id"], 1):
            html = build_assignment_reminder_html(a["student_name"], a)
            subject = f"⏰ Reminder: '{a['title']}' is due tomorrow!"
            if send_email(a["student_email"], subject, html):
                _log_notification(a["user_id"], "assignment", a["id"], 1)
    print(f"[SCHEDULER]   Checked {len(assignments)} assignment(s) due tomorrow.")

    # ---- Exam reminders (3 days before) ----
    exams_3d = execute_query(
        "SELECT e.*, u.name AS student_name, u.email AS student_email "
        "FROM exams e JOIN users u ON e.user_id = u.id "
        "WHERE e.exam_date = %s",
        (three_days,),
        fetch=True,
    )
    for e in exams_3d:
        if not _already_notified(e["user_id"], "exam", e["id"], 3):
            html = build_exam_reminder_html(e["student_name"], e, 3)
            subject = f"📝 Exam in 3 days: {e['title']}"
            if send_email(e["student_email"], subject, html):
                _log_notification(e["user_id"], "exam", e["id"], 3)
    print(f"[SCHEDULER]   Checked {len(exams_3d)} exam(s) in 3 days.")

    # ---- Exam reminders (1 day before) ----
    exams_1d = execute_query(
        "SELECT e.*, u.name AS student_name, u.email AS student_email "
        "FROM exams e JOIN users u ON e.user_id = u.id "
        "WHERE e.exam_date = %s",
        (tomorrow,),
        fetch=True,
    )
    for e in exams_1d:
        if not _already_notified(e["user_id"], "exam", e["id"], 1):
            html = build_exam_reminder_html(e["student_name"], e, 1)
            subject = f"🚨 Exam TOMORROW: {e['title']}"
            if send_email(e["student_email"], subject, html):
                _log_notification(e["user_id"], "exam", e["id"], 1)
    print(f"[SCHEDULER]   Checked {len(exams_1d)} exam(s) tomorrow.")
    print("[SCHEDULER] Reminder check complete.")


def init_scheduler(app):
    """
    Set up APScheduler:
      - If REMINDER_CHECK_INTERVAL_MINUTES is set → run every N minutes (demo mode).
      - Otherwise → run once daily at REMINDER_HOUR:REMINDER_MINUTE.
    Also runs the check once at startup.
    """
    scheduler = BackgroundScheduler(daemon=True)

    interval = os.getenv("REMINDER_CHECK_INTERVAL_MINUTES", "").strip()
    hour = int(os.getenv("REMINDER_HOUR", 8))
    minute = int(os.getenv("REMINDER_MINUTE", 0))

    if interval and interval.isdigit():
        # Demo mode – frequent checks
        mins = int(interval)
        scheduler.add_job(run_reminder_check, "interval", minutes=mins, id="reminder_interval")
        print(f"[SCHEDULER] Demo mode: checking every {mins} minute(s).")
    else:
        # Production mode – once daily
        scheduler.add_job(
            run_reminder_check, "cron", hour=hour, minute=minute, id="reminder_daily"
        )
        print(f"[SCHEDULER] Daily check scheduled at {hour:02d}:{minute:02d}.")

    scheduler.start()
    print("[SCHEDULER] Scheduler started. Running initial check now...")

    # Run once at startup (inside app context is fine since we don't use Flask-specific features)
    try:
        run_reminder_check()
    except Exception as e:
        print(f"[SCHEDULER] Initial check failed (DB may not be ready): {e}")
