"""
app.py – Main Flask application for StudyTrack.
Two-tier architecture: Flask (Tier 1) ↔ MySQL (Tier 2).
"""

import os
from datetime import date, datetime, timedelta
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load .env file (works locally; in Docker the env vars come from compose)
load_dotenv()

from db import get_connection, execute_query
from mailer import send_email, build_assignment_reminder_html, build_exam_reminder_html, is_smtp_configured
from scheduler import init_scheduler, run_reminder_check

# ============================================================
# Flask App Setup
# ============================================================
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-dev-key")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)

# ============================================================
# Login Required Decorator
# ============================================================
def login_required(f):
    """Redirect to login page if user is not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ============================================================
# HEALTH CHECK  (used by Docker healthcheck)
# ============================================================
@app.route("/health")
def health():
    """Return 200 if the app can reach the database."""
    try:
        conn = get_connection(retries=1, delay=1)
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# ============================================================
# AUTH ROUTES
# ============================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new student account."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        # Validation
        if not all([name, email, password, confirm]):
            flash("All fields are required.", "danger")
            return render_template("register.html")
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html")

        # Check if email already exists
        existing = execute_query("SELECT id FROM users WHERE email=%s", (email,), fetch=True)
        if existing:
            flash("An account with this email already exists.", "danger")
            return render_template("register.html")

        # Create user
        hashed = generate_password_hash(password)
        execute_query(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, hashed), commit=True
        )
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in an existing user."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        rows = execute_query("SELECT * FROM users WHERE email=%s", (email,), fetch=True)
        if rows and check_password_hash(rows[0]["password_hash"], password):
            session.permanent = True
            session["user_id"] = rows[0]["id"]
            session["user_name"] = rows[0]["name"]
            session["user_email"] = rows[0]["email"]
            flash(f"Welcome back, {rows[0]['name']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clear the session and log out."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ============================================================
# DASHBOARD
# ============================================================
@app.route("/")
@login_required
def dashboard():
    """Main dashboard with summary cards, deadlines, and progress."""
    uid = session["user_id"]
    today = date.today()

    # Fetch all assignments for this user
    assignments = execute_query(
        "SELECT * FROM assignments WHERE user_id=%s ORDER BY due_date ASC", (uid,), fetch=True
    )
    # Fetch upcoming exams
    exams = execute_query(
        "SELECT * FROM exams WHERE user_id=%s AND exam_date >= %s ORDER BY exam_date ASC",
        (uid, today), fetch=True
    )

    # Summary stats
    total = len(assignments)
    completed = sum(1 for a in assignments if a["status"] == "Completed")
    pending = sum(1 for a in assignments if a["status"] != "Completed")
    overdue = sum(1 for a in assignments if a["status"] != "Completed" and a["due_date"] < today)
    week_end = today + timedelta(days=7)
    due_this_week = sum(
        1 for a in assignments
        if a["status"] != "Completed" and today <= a["due_date"] <= week_end
    )
    progress = round((completed / total) * 100) if total > 0 else 0

    # Upcoming deadlines (non-completed, sorted by due date)
    upcoming = [a for a in assignments if a["status"] != "Completed"]
    for a in upcoming:
        delta = (a["due_date"] - today).days
        a["days_left"] = delta
        if delta <= 1:
            a["badge_class"] = "bg-danger"
        elif delta <= 3:
            a["badge_class"] = "bg-warning text-dark"
        else:
            a["badge_class"] = "bg-success"

    # Exams with countdown
    for e in exams:
        e["days_left"] = (e["exam_date"] - today).days

    # Collect unique subjects for filters
    subjects = sorted(set(a["subject"] for a in assignments))

    return render_template(
        "dashboard.html",
        assignments=assignments, upcoming=upcoming, exams=exams,
        total=total, completed=completed, pending=pending,
        overdue=overdue, due_this_week=due_this_week, progress=progress,
        subjects=subjects, today=today
    )

# ============================================================
# ASSIGNMENTS CRUD
# ============================================================
@app.route("/assignments")
@login_required
def assignments_list():
    """List all assignments with filters."""
    uid = session["user_id"]

    # Get filter params
    subject_filter = request.args.get("subject", "")
    priority_filter = request.args.get("priority", "")
    status_filter = request.args.get("status", "")
    search_q = request.args.get("q", "").strip()
    sort_by = request.args.get("sort", "due_date")

    # Build query dynamically
    query = "SELECT * FROM assignments WHERE user_id=%s"
    params = [uid]

    if subject_filter:
        query += " AND subject=%s"
        params.append(subject_filter)
    if priority_filter:
        query += " AND priority=%s"
        params.append(priority_filter)
    if status_filter:
        query += " AND status=%s"
        params.append(status_filter)
    if search_q:
        query += " AND (title LIKE %s OR description LIKE %s)"
        params.extend([f"%{search_q}%", f"%{search_q}%"])

    # Sorting
    if sort_by == "priority":
        query += " ORDER BY FIELD(priority, 'High', 'Medium', 'Low'), due_date ASC"
    else:
        query += " ORDER BY due_date ASC"

    assignments = execute_query(query, tuple(params), fetch=True)

    # Add days_left for display
    today = date.today()
    for a in assignments:
        delta = (a["due_date"] - today).days
        a["days_left"] = delta
        if delta <= 1:
            a["badge_class"] = "bg-danger"
        elif delta <= 3:
            a["badge_class"] = "bg-warning text-dark"
        else:
            a["badge_class"] = "bg-success"

    # Get unique subjects for filter dropdown
    all_assignments = execute_query(
        "SELECT DISTINCT subject FROM assignments WHERE user_id=%s ORDER BY subject",
        (uid,), fetch=True
    )
    subjects = [a["subject"] for a in all_assignments]

    return render_template(
        "assignments.html", assignments=assignments, subjects=subjects,
        subject_filter=subject_filter, priority_filter=priority_filter,
        status_filter=status_filter, search_q=search_q, sort_by=sort_by,
        today=today
    )


@app.route("/assignments/add", methods=["POST"])
@login_required
def assignment_add():
    """Add a new assignment."""
    uid = session["user_id"]
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date", "")
    priority = request.form.get("priority", "Medium")
    status = request.form.get("status", "Pending")

    if not all([title, subject, due_date]):
        flash("Title, subject, and due date are required.", "danger")
        return redirect(url_for("assignments_list"))

    execute_query(
        "INSERT INTO assignments (user_id, title, subject, description, due_date, priority, status) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (uid, title, subject, description, due_date, priority, status),
        commit=True
    )
    flash(f"Assignment '{title}' added!", "success")
    return redirect(url_for("assignments_list"))


@app.route("/assignments/edit/<int:aid>", methods=["POST"])
@login_required
def assignment_edit(aid):
    """Edit an existing assignment."""
    uid = session["user_id"]
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date", "")
    priority = request.form.get("priority", "Medium")
    status = request.form.get("status", "Pending")

    execute_query(
        "UPDATE assignments SET title=%s, subject=%s, description=%s, "
        "due_date=%s, priority=%s, status=%s WHERE id=%s AND user_id=%s",
        (title, subject, description, due_date, priority, status, aid, uid),
        commit=True
    )
    flash(f"Assignment '{title}' updated!", "success")
    return redirect(url_for("assignments_list"))


@app.route("/assignments/delete/<int:aid>", methods=["POST"])
@login_required
def assignment_delete(aid):
    """Delete an assignment."""
    uid = session["user_id"]
    execute_query("DELETE FROM assignments WHERE id=%s AND user_id=%s", (aid, uid), commit=True)
    flash("Assignment deleted.", "info")
    return redirect(url_for("assignments_list"))


@app.route("/assignments/toggle/<int:aid>", methods=["POST"])
@login_required
def assignment_toggle(aid):
    """Toggle assignment status to Completed or back to Pending."""
    uid = session["user_id"]
    rows = execute_query(
        "SELECT status FROM assignments WHERE id=%s AND user_id=%s", (aid, uid), fetch=True
    )
    if rows:
        new_status = "Completed" if rows[0]["status"] != "Completed" else "Pending"
        execute_query(
            "UPDATE assignments SET status=%s WHERE id=%s AND user_id=%s",
            (new_status, aid, uid), commit=True
        )
        flash(f"Assignment marked as {new_status}.", "success")
    return redirect(request.referrer or url_for("assignments_list"))

# ============================================================
# EXAMS CRUD
# ============================================================
@app.route("/exams")
@login_required
def exams_list():
    """List all exams."""
    uid = session["user_id"]
    today = date.today()

    subject_filter = request.args.get("subject", "")
    type_filter = request.args.get("exam_type", "")
    search_q = request.args.get("q", "").strip()

    query = "SELECT * FROM exams WHERE user_id=%s"
    params = [uid]

    if subject_filter:
        query += " AND subject=%s"
        params.append(subject_filter)
    if type_filter:
        query += " AND exam_type=%s"
        params.append(type_filter)
    if search_q:
        query += " AND (title LIKE %s OR syllabus LIKE %s)"
        params.extend([f"%{search_q}%", f"%{search_q}%"])

    query += " ORDER BY exam_date ASC"
    exams = execute_query(query, tuple(params), fetch=True)

    for e in exams:
        e["days_left"] = (e["exam_date"] - today).days

    # Subjects for filter
    all_exams = execute_query(
        "SELECT DISTINCT subject FROM exams WHERE user_id=%s ORDER BY subject",
        (uid,), fetch=True
    )
    subjects = [e["subject"] for e in all_exams]

    return render_template(
        "exams.html", exams=exams, subjects=subjects,
        subject_filter=subject_filter, type_filter=type_filter,
        search_q=search_q, today=today
    )


@app.route("/exams/add", methods=["POST"])
@login_required
def exam_add():
    """Add a new exam."""
    uid = session["user_id"]
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    exam_type = request.form.get("exam_type", "Quiz")
    exam_date = request.form.get("exam_date", "")
    exam_time = request.form.get("exam_time", "") or None
    syllabus = request.form.get("syllabus", "").strip()
    venue = request.form.get("venue", "").strip()

    if not all([title, subject, exam_date]):
        flash("Title, subject, and exam date are required.", "danger")
        return redirect(url_for("exams_list"))

    execute_query(
        "INSERT INTO exams (user_id, title, subject, exam_type, exam_date, exam_time, syllabus, venue) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (uid, title, subject, exam_type, exam_date, exam_time, syllabus, venue),
        commit=True
    )
    flash(f"Exam '{title}' added!", "success")
    return redirect(url_for("exams_list"))


@app.route("/exams/edit/<int:eid>", methods=["POST"])
@login_required
def exam_edit(eid):
    """Edit an existing exam."""
    uid = session["user_id"]
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    exam_type = request.form.get("exam_type", "Quiz")
    exam_date = request.form.get("exam_date", "")
    exam_time = request.form.get("exam_time", "") or None
    syllabus = request.form.get("syllabus", "").strip()
    venue = request.form.get("venue", "").strip()

    execute_query(
        "UPDATE exams SET title=%s, subject=%s, exam_type=%s, exam_date=%s, "
        "exam_time=%s, syllabus=%s, venue=%s WHERE id=%s AND user_id=%s",
        (title, subject, exam_type, exam_date, exam_time, syllabus, venue, eid, uid),
        commit=True
    )
    flash(f"Exam '{title}' updated!", "success")
    return redirect(url_for("exams_list"))


@app.route("/exams/delete/<int:eid>", methods=["POST"])
@login_required
def exam_delete(eid):
    """Delete an exam."""
    uid = session["user_id"]
    execute_query("DELETE FROM exams WHERE id=%s AND user_id=%s", (eid, uid), commit=True)
    flash("Exam deleted.", "info")
    return redirect(url_for("exams_list"))

# ============================================================
# SETTINGS PAGE
# ============================================================
@app.route("/settings")
@login_required
def settings():
    """Settings page with test email and manual reminder check."""
    smtp_configured = is_smtp_configured()
    interval = os.getenv("REMINDER_CHECK_INTERVAL_MINUTES", "")
    return render_template("settings.html", smtp_configured=smtp_configured, interval=interval)


@app.route("/settings/test-email", methods=["POST"])
@login_required
def test_email():
    """Send a test email to the logged-in user."""
    email = session.get("user_email", "")
    name = session.get("user_name", "Student")
    subject = "🧪 StudyTrack Test Email"
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto;
                padding: 24px; background: #f8f9fa; border-radius: 12px;">
        <h2 style="color: #667eea;">✅ Test Email Successful!</h2>
        <p>Hi <strong>{name}</strong>,</p>
        <p>If you're reading this, your SMTP settings are working correctly.</p>
        <p style="color: #888; font-size: 13px;">— StudyTrack Notification System</p>
    </div>
    """
    if send_email(email, subject, html):
        flash("Test email sent! Check your inbox (or the console logs).", "success")
    else:
        flash("Failed to send test email. Check your SMTP settings.", "danger")
    return redirect(url_for("settings"))


@app.route("/settings/run-check", methods=["POST"])
@login_required
def manual_check():
    """Manually trigger the reminder check."""
    try:
        run_reminder_check()
        flash("Reminder check completed! Check the console logs for details.", "success")
    except Exception as e:
        flash(f"Reminder check failed: {e}", "danger")
    return redirect(url_for("settings"))

# ============================================================
# API ENDPOINT – Get assignment data (for edit modal)
# ============================================================
@app.route("/api/assignment/<int:aid>")
@login_required
def api_get_assignment(aid):
    """Return assignment data as JSON for the edit modal."""
    uid = session["user_id"]
    rows = execute_query(
        "SELECT * FROM assignments WHERE id=%s AND user_id=%s", (aid, uid), fetch=True
    )
    if rows:
        a = rows[0]
        # Convert date objects to strings for JSON
        a["due_date"] = str(a["due_date"])
        a["created_at"] = str(a["created_at"])
        a["updated_at"] = str(a["updated_at"])
        return jsonify(a)
    return jsonify({"error": "Not found"}), 404


@app.route("/api/exam/<int:eid>")
@login_required
def api_get_exam(eid):
    """Return exam data as JSON for the edit modal."""
    uid = session["user_id"]
    rows = execute_query(
        "SELECT * FROM exams WHERE id=%s AND user_id=%s", (eid, uid), fetch=True
    )
    if rows:
        e = rows[0]
        e["exam_date"] = str(e["exam_date"])
        e["exam_time"] = str(e["exam_time"]) if e["exam_time"] else ""
        e["created_at"] = str(e["created_at"])
        e["updated_at"] = str(e["updated_at"])
        return jsonify(e)
    return jsonify({"error": "Not found"}), 404

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    # Initialize the reminder scheduler
    init_scheduler(app)
    port = int(os.getenv("APP_PORT", 8085))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
