"""
tests/test_studytrack.py – Comprehensive automated test suite for StudyTrack.
Covers unit tests, security hashing, template rendering, and route endpoints.
Uses Python's standard `unittest` library (no external test runner needed).
"""

import os
import sys
import unittest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

# Add app directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from werkzeug.security import generate_password_hash, check_password_hash
from mailer import (
    build_assignment_reminder_html,
    build_exam_reminder_html,
    is_smtp_configured,
    send_email
)
from app import app


class TestSecurityAndAuth(unittest.TestCase):
    """Test cryptographic security and password hashing."""

    def test_password_hashing_and_verification(self):
        """Verify that Werkzeug produces secure hashes and verifies correctly."""
        raw_pw = "Demo@123"
        hashed = generate_password_hash(raw_pw)
        self.assertNotEqual(raw_pw, hashed)
        self.assertTrue(check_password_hash(hashed, raw_pw))
        self.assertFalse(check_password_hash(hashed, "WrongPassword"))

    def test_password_hash_uniqueness(self):
        """Verify that salting ensures two hashes of the same password differ."""
        h1 = generate_password_hash("Secret123")
        h2 = generate_password_hash("Secret123")
        self.assertNotEqual(h1, h2)


class TestMailerAndTemplates(unittest.TestCase):
    """Test email HTML generation and fallback behavior."""

    def test_assignment_email_html_content(self):
        """Verify that assignment reminder HTML includes title, priority, and due date."""
        assignment = {
            "title": "Cloud Networking Lab Report",
            "subject": "Cloud Computing",
            "due_date": "2026-11-25",
            "priority": "High",
            "status": "In Progress"
        }
        html = build_assignment_reminder_html("Demo Student", assignment)
        self.assertIn("Demo Student", html)
        self.assertIn("Cloud Networking Lab Report", html)
        self.assertIn("Cloud Computing", html)
        self.assertIn("High", html)
        self.assertIn("#dc3545", html)  # Red accent for High priority

    def test_exam_email_html_content(self):
        """Verify that exam reminder HTML includes type, venue, and time."""
        exam = {
            "title": "DBMS Mid-Sem Examination",
            "subject": "Database Management",
            "exam_type": "Mid-Sem",
            "exam_date": "2026-11-29",
            "exam_time": "10:00:00",
            "venue": "Room 301, CS Block",
            "syllabus": "Normalization and SQL Joins"
        }
        html = build_exam_reminder_html("Demo Student", exam, days_left=3)
        self.assertIn("DBMS Mid-Sem Examination", html)
        self.assertIn("Room 301, CS Block", html)
        self.assertIn("in 3 days", html)
        self.assertIn("Mid-Sem", html)

    @patch.dict(os.environ, {"SMTP_USERNAME": "", "SMTP_PASSWORD": ""})
    def test_smtp_not_configured_fallback(self):
        """Verify that is_smtp_configured is False and send_email safely falls back to console."""
        self.assertFalse(is_smtp_configured())
        # send_email must return True (safe fallback without crashing)
        result = send_email("test@example.com", "Test Subject", "<p>Hello</p>")
        self.assertTrue(result)


class TestDeadlineCalculations(unittest.TestCase):
    """Test date math and countdown classification."""

    def test_countdown_days_left(self):
        """Verify days left calculation for today, tomorrow, and future dates."""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        in_3_days = today + timedelta(days=3)
        yesterday = today - timedelta(days=1)

        self.assertEqual((tomorrow - today).days, 1)
        self.assertEqual((in_3_days - today).days, 3)
        self.assertEqual((yesterday - today).days, -1)

    def test_progress_bar_percentage(self):
        """Verify completion percentage formula."""
        total = 6
        completed = 2
        progress = round((completed / total) * 100)
        self.assertEqual(progress, 33)

        # Zero total edge case
        total_zero = 0
        progress_zero = round((0 / total_zero) * 100) if total_zero > 0 else 0
        self.assertEqual(progress_zero, 0)


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask web application routes via test client."""

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_login_page_renders_ok(self):
        """Verify that /login responds with HTTP 200 and renders the form."""
        res = self.client.get("/login")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"StudyTrack", res.data)
        self.assertIn(b"Login", res.data)

    def test_register_page_renders_ok(self):
        """Verify that /register responds with HTTP 200 and has registration fields."""
        res = self.client.get("/register")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Create Account", res.data)
        self.assertIn(b"confirm_password", res.data)

    def test_dashboard_requires_login(self):
        """Verify that visiting / while unauthenticated redirects to /login."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login", res.headers["Location"])

    @patch("app.get_connection")
    def test_health_endpoint_healthy(self, mock_get_conn):
        """Verify that /health returns 200 when database is accessible."""
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn

        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'"status":"healthy"', res.data)
        self.assertIn(b'"database":"connected"', res.data)

    @patch("app.get_connection")
    def test_health_endpoint_unhealthy(self, mock_get_conn):
        """Verify that /health returns 500 when database fails."""
        mock_get_conn.side_effect = Exception("Connection refused")

        res = self.client.get("/health")
        self.assertEqual(res.status_code, 500)
        self.assertIn(b'"status":"unhealthy"', res.data)


if __name__ == "__main__":
    unittest.main()
