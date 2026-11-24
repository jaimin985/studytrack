"""
generate_presentation.py – Generates StudyTrack_Presentation.pptx
using python-pptx with 15 professional slides, vector shapes,
embedded real screenshots, and clear formatting.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Initialize Presentation with 16:9 widescreen
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors
NAVY = RGBColor(26, 35, 126)        # #1A237E
INDIGO = RGBColor(63, 81, 181)      # #3F51B5
TEAL = RGBColor(0, 150, 136)        # #009688
DARK_GRAY = RGBColor(33, 33, 33)    # #212121
LIGHT_BG = RGBColor(245, 247, 250)  # #F5F7FA
WHITE = RGBColor(255, 255, 255)
ACCENT_ORANGE = RGBColor(255, 112, 67) # #FF7043
CARD_BG = RGBColor(255, 255, 255)
BORDER_COLOR = RGBColor(224, 224, 224)

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "docs", "screenshots")

def set_slide_bg(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="STUDYTRACK • CLOUD COMPUTING LAB"):
    # Header bar background
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = TEAL
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY

def add_card(slide, left, top, width, height, title, items, border_color=BORDER_COLOR):
    # Shape container
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)
    tf.margin_right = Inches(0.25)
    tf.margin_bottom = Inches(0.2)
    
    if title:
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY
        p_title.space_after = Pt(10)
    
    for i, item in enumerate(items):
        p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
        p.text = "• " + item
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(8)

# ============================================================
# SLIDE 1: Title Slide
# ============================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_bg(s1, NAVY)

# Main Title Container
t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(3.0))
tf1 = t_box.text_frame
tf1.word_wrap = True

p_sub = tf1.paragraphs[0]
p_sub.text = "CLOUD COMPUTING LAB PROJECT • TWO-TIER ARCHITECTURE"
p_sub.font.size = Pt(14)
p_sub.font.bold = True
p_sub.font.color.rgb = TEAL

p_main = tf1.add_paragraph()
p_main.text = "StudyTrack: Student Assignment & Exam Tracker"
p_main.font.size = Pt(36)
p_main.font.bold = True
p_main.font.color.rgb = WHITE
p_main.space_after = Pt(12)

p_desc = tf1.add_paragraph()
p_desc.text = "A Containerized Two-Tier Web Application with Automated Email Reminders Built on Docker & Docker Compose"
p_desc.font.size = Pt(16)
p_desc.font.color.rgb = RGBColor(197, 202, 233)

# Team details box
team_box = s1.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(11.3), Inches(2.0))
tft = team_box.text_frame
tft.word_wrap = True

pt1 = tft.paragraphs[0]
pt1.text = "Project Team Members:"
pt1.font.size = Pt(13)
pt1.font.bold = True
pt1.font.color.rgb = ACCENT_ORANGE

members = [
    "Team Member 1: [STUDENT NAME 1] (Roll No: [ROLL-001])",
    "Team Member 2: [STUDENT NAME 2] (Roll No: [ROLL-002])",
    "Team Member 3: [STUDENT NAME 3] (Roll No: [ROLL-003])",
    "Course: Cloud Computing Lab | Semester: [SEMESTER] | Faculty Guide: [PROFESSOR NAME]"
]
for m in members:
    pm = tft.add_paragraph()
    pm.text = m
    pm.font.size = Pt(12)
    pm.font.color.rgb = WHITE

# ============================================================
# SLIDE 2: Problem Statement
# ============================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_bg(s2, LIGHT_BG)
add_header(s2, "Problem Statement & Student Motivation")

add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "The Academic Deadlines Dilemma", [
    "University students juggle 5-7 courses concurrently, each with separate deadlines.",
    "Assignments, weekly quizzes, lab assessments, and mid-terms lead to cognitive overload.",
    "Deadlines are tracked across disparate WhatsApp chats, LMS portals, and scattered notes.",
    "Result: Missed submissions, rushed low-quality work, and unnecessary academic stress."
])

add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "Limitations of Basic Cloud Lab Tutorials", [
    "Standard lab tutorials feature trivial single-page apps (e.g. basic guestbook with one button).",
    "Lacks real-world student utility, relational modeling, or role-based user isolation.",
    "No asynchronous automation or background notification processing.",
    "Goal: Build a production-grade, two-tier web application solving real student needs."
])

# ============================================================
# SLIDE 3: Our Solution & Key Features
# ============================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_bg(s3, LIGHT_BG)
add_header(s3, "StudyTrack Solution & Key Capabilities")

add_card(s3, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
         "User & Task Management", [
    "Session Authentication: Secure registration & login with Werkzeug password hashing.",
    "Strict Tenant Isolation: Each student only accesses their own assignments and exams.",
    "Full CRUD Operations: Create, edit, delete, and toggle completion with a single click.",
    "Subject & Priority Tagging: Color-coded High, Medium, and Low urgency badges."
])

add_card(s3, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
         "Intelligent Dashboard", [
    "Live Summary Cards: Pending count, due this week, overdue tasks, and completed items.",
    "Dynamic Completion Bar: Real-time calculation of completed task percentage.",
    "Urgency Countdown: Color-coded alerts (Red ≤1d, Orange ≤3d, Green >3d).",
    "Smart Sorting & Filtering: Filter by subject, priority, status, and keyword search."
])

add_card(s3, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
         "Proactive Automation", [
    "Background Scheduler: APScheduler engine running daily at 08:00 AM.",
    "Tiered Exam Reminders: Multi-stage emails sent 3 days before and 1 day before.",
    "Deduplication Log: SQL notification_log prevents duplicate reminders.",
    "Demo Mode: Configurable 1-minute interval and manual 'Run Check' trigger."
])

# ============================================================
# SLIDE 4: Why Two-Tier Architecture?
# ============================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_bg(s4, LIGHT_BG)
add_header(s4, "Why Two-Tier Architecture in Cloud Computing?")

add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "Separation of Concerns & Modularity", [
    "Tier 1 (Presentation & Logic): Flask + Gunicorn handles HTTP, routing, rendering, & jobs.",
    "Tier 2 (Persistence Tier): Dedicated MySQL 8.0 engine dedicated entirely to data integrity.",
    "Stateless Application Tier: Web containers can be killed, updated, or scaled without loss.",
    "Independent Lifecycle: App code can be deployed without restarting or modifying database."
])

add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "Cloud-Native Benefits Demonstrated", [
    "Security Isolation: Database port 3306 is not exposed to public traffic; sits on private bridge network.",
    "Persistent Named Volume: MySQL storage outlives container recreation (survives docker compose down).",
    "Orchestration with Compose: Single declarative YAML configuration initializes both tiers seamlessly.",
    "Foundation for Cloud Migration: Directly maps to AWS ECS (Web Tier) + AWS RDS MySQL (Database Tier)."
])

# ============================================================
# SLIDE 5: Architecture Diagram (Vector Shapes)
# ============================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_bg(s5, LIGHT_BG)
add_header(s5, "System Architecture & Network Topology")

# Draw diagram containers and connections
# 1. User Browser
box_browser = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.0), Inches(2.2), Inches(1.8))
box_browser.fill.solid()
box_browser.fill.fore_color.rgb = WHITE
box_browser.line.color.rgb = INDIGO
box_browser.line.width = Pt(2)
tf_b = box_browser.text_frame
tf_b.text = "CLIENT TIER\n\nStudent Browser\n(macOS / Chrome)\nhttp://localhost:8085"
tf_b.paragraphs[0].font.size = Pt(13)
tf_b.paragraphs[0].font.bold = True
tf_b.paragraphs[0].font.color.rgb = NAVY

# 2. Host Port Mapping Arrow
arr1 = s5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.1), Inches(3.6), Inches(1.0), Inches(0.6))
arr1.fill.solid()
arr1.fill.fore_color.rgb = TEAL
arr1.line.fill.background()

# 3. Docker Bridge Network Boundary
docker_net = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.2), Inches(1.8), Inches(5.8), Inches(5.0))
docker_net.fill.solid()
docker_net.fill.fore_color.rgb = RGBColor(232, 234, 246)
docker_net.line.color.rgb = INDIGO
docker_net.line.width = Pt(1.5)
tf_net = docker_net.text_frame
tf_net.text = "DOCKER BRIDGE NETWORK: studytrack-network (Subnet: 172.19.0.0/16)"
tf_net.paragraphs[0].font.size = Pt(11)
tf_net.paragraphs[0].font.bold = True
tf_net.paragraphs[0].font.color.rgb = INDIGO

# Tier 1 Container
box_web = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(2.5), Inches(2.4), Inches(3.8))
box_web.fill.solid()
box_web.fill.fore_color.rgb = WHITE
box_web.line.color.rgb = TEAL
box_web.line.width = Pt(2)
tf_w = box_web.text_frame
tf_w.text = "TIER 1: WEB CONTAINER\n(studytrack-web)\n\n• Python 3.11-slim\n• Gunicorn WSGI\n• Flask Routes\n• Jinja2 Templates\n• APScheduler\n• Healthcheck (:8085)"
tf_w.paragraphs[0].font.size = Pt(12)
tf_w.paragraphs[0].font.bold = True
tf_w.paragraphs[0].font.color.rgb = NAVY

# Arrow between Web and DB
arr2 = s5.shapes.add_shape(MSO_SHAPE.LEFT_RIGHT_ARROW, Inches(7.0), Inches(4.1), Inches(0.8), Inches(0.6))
arr2.fill.solid()
arr2.fill.fore_color.rgb = NAVY
arr2.line.fill.background()

# Tier 2 Container
box_db = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(2.5), Inches(1.9), Inches(3.8))
box_db.fill.solid()
box_db.fill.fore_color.rgb = WHITE
box_db.line.color.rgb = ACCENT_ORANGE
box_db.line.width = Pt(2)
tf_d = box_db.text_frame
tf_d.text = "TIER 2: DATABASE\n(studytrack-db)\n\n• MySQL 8.0 Engine\n• Port 3306 (Internal)\n• Host: 3307 (Admin)\n• init.sql Seed\n• Healthcheck"
tf_d.paragraphs[0].font.size = Pt(12)
tf_d.paragraphs[0].font.bold = True
tf_d.paragraphs[0].font.color.rgb = NAVY

# 4. Storage Volume
box_vol = s5.shapes.add_shape(MSO_SHAPE.CAN, Inches(10.3), Inches(4.2), Inches(2.3), Inches(2.1))
box_vol.fill.solid()
box_vol.fill.fore_color.rgb = WHITE
box_vol.line.color.rgb = ACCENT_ORANGE
box_vol.line.width = Pt(2)
tf_v = box_vol.text_frame
tf_v.text = "NAMED VOLUME\nstudytrack-db-data\n\nPersists /var/lib/mysql\nSurvives Container Restarts"
tf_v.paragraphs[0].font.size = Pt(11)
tf_v.paragraphs[0].font.bold = True
tf_v.paragraphs[0].font.color.rgb = DARK_GRAY

# 5. External SMTP
box_smtp = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.3), Inches(1.8), Inches(2.3), Inches(2.0))
box_smtp.fill.solid()
box_smtp.fill.fore_color.rgb = WHITE
box_smtp.line.color.rgb = TEAL
box_smtp.line.width = Pt(2)
tf_s = box_smtp.text_frame
tf_s.text = "EXTERNAL SERVICE\nGmail SMTP Server\n(Port 587 TLS)\n\n• Dispatches HTML Emails\n• Safe Console Fallback"
tf_s.paragraphs[0].font.size = Pt(11)
tf_s.paragraphs[0].font.bold = True
tf_s.paragraphs[0].font.color.rgb = NAVY

# ============================================================
# SLIDE 6: Tech Stack
# ============================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_bg(s6, LIGHT_BG)
add_header(s6, "Technology Stack & Frameworks")

add_card(s6, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
         "Tier 1: Web & App Server", [
    "Python 3.11-slim: Lightweight, secure container base.",
    "Flask 3.0: Minimalist WSGI web framework with clean routing.",
    "Gunicorn 21.2: Production WSGI HTTP server with worker threads.",
    "Werkzeug 3.0: Cryptographic password hashing (scrypt algorithm).",
    "Jinja2: Server-rendered templates with clean component structure."
])

add_card(s6, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
         "Tier 2 & Infrastructure", [
    "MySQL 8.0: ACID-compliant relational storage engine.",
    "mysql-connector-python: Pure Python native database driver.",
    "Docker Desktop (macOS): Apple Silicon (ARM64) & Intel support.",
    "Docker Compose v2: Declarative multi-container orchestration.",
    "Custom Bridge Network: Isolated container-to-container DNS."
])

add_card(s6, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
         "Automation & Frontend", [
    "APScheduler 3.10: In-process cron & interval background job engine.",
    "Python smtplib: TLS-encrypted SMTP delivery with console fallback.",
    "Bootstrap 5.3: Modern responsive UI grid, cards, and modal dialogs.",
    "Bootstrap Icons: Cohesive visual cues and status indicators.",
    "Vanilla JS: Async fetch API for dynamic modal updates."
])

# ============================================================
# SLIDE 7: Database Schema (ER Structure)
# ============================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_bg(s7, LIGHT_BG)
add_header(s7, "Relational Database Schema & Integrity")

add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
         "users Table", [
    "id (INT AUTO_INCREMENT PRIMARY KEY)",
    "name (VARCHAR 100), email (VARCHAR 150 UNIQUE)",
    "password_hash (VARCHAR 255 - scrypt hashed)",
    "created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
])

add_card(s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.4),
         "notification_log Table (Deduplication)", [
    "id (INT PRIMARY KEY), user_id (INT FK -> users.id)",
    "item_type (ENUM 'assignment', 'exam'), item_id (INT)",
    "days_before (INT - e.g. 1 or 3), sent_at (TIMESTAMP)",
    "UNIQUE KEY uq_notification (user_id, item_type, item_id, days_before)"
])

add_card(s7, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
         "assignments Table", [
    "id (INT PRIMARY KEY), user_id (INT FK -> users.id ON DELETE CASCADE)",
    "title (VARCHAR 200), subject (VARCHAR 100), description (TEXT)",
    "due_date (DATE), priority (ENUM High/Med/Low), status (Pending/Completed)",
    "INDEX idx_user_status, idx_user_due"
])

add_card(s7, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.4),
         "exams Table", [
    "id (INT PRIMARY KEY), user_id (INT FK -> users.id ON DELETE CASCADE)",
    "title (VARCHAR 200), subject (VARCHAR 100), exam_type (Quiz/Mid-Sem/etc)",
    "exam_date (DATE), exam_time (TIME), syllabus (TEXT), venue (VARCHAR)",
    "INDEX idx_user_exam_date"
])

# ============================================================
# SLIDE 8: Docker & Compose Setup
# ============================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_bg(s8, LIGHT_BG)
add_header(s8, "Docker Containerization & Orchestration")

add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "Dockerfile Highlights", [
    "Base Image: python:3.11-slim (minimal attack surface, ~150MB).",
    "Security: Non-root user 'studytrack' created and used at runtime.",
    "Layer Caching: requirements.txt copied and installed before source code.",
    "Preloaded Gunicorn: Starts WSGI server with single worker for scheduler safety.",
    "Container Healthcheck: Internal Python urllib checks /health every 30s."
])

add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "docker-compose.yml Highlights", [
    "Custom Bridge Network: 'studytrack-net' allows DNS lookup via service names.",
    "Health-Based Dependency: web service waits for db: condition: service_healthy.",
    "Persistent Named Volume: 'studytrack-db-data' mounts to /var/lib/mysql.",
    "Automated Schema Seeding: ./db/init.sql mounts to /docker-entrypoint-initdb.d/.",
    "Environment Driven: All credentials and ports parameterized via .env."
])

# ============================================================
# SLIDE 9: Real Screenshots: Dashboard & Add Modal
# ============================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_bg(s9, LIGHT_BG)
add_header(s9, "Application Showcase: Interactive Dashboard")

dash_img = os.path.join(SCREENSHOT_DIR, "03_dashboard.png")
if os.path.exists(dash_img):
    s9.shapes.add_picture(dash_img, Inches(0.8), Inches(1.8), Inches(7.5), Inches(4.8))

add_card(s9, Inches(8.6), Inches(1.8), Inches(3.9), Inches(4.8),
         "Dashboard Highlights", [
    "Live metric counters for Pending, Due This Week, Overdue, and Completed.",
    "Interactive Progress Bar computing completion percentage dynamically.",
    "Urgent Deadlines list with colour-coded urgency pills.",
    "Upcoming Exams panel featuring multi-day countdown indicators.",
    "Clean top action buttons for instant assignment and exam creation."
])

# ============================================================
# SLIDE 10: Real Screenshots: Assignments & Exams
# ============================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_bg(s10, LIGHT_BG)
add_header(s10, "Application Showcase: Assignments & Exams")

assign_img = os.path.join(SCREENSHOT_DIR, "06_assignments_filtered.png")
if os.path.exists(assign_img):
    s10.shapes.add_picture(assign_img, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))

exam_img = os.path.join(SCREENSHOT_DIR, "07_exams.png")
if os.path.exists(exam_img):
    s10.shapes.add_picture(exam_img, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))

# ============================================================
# SLIDE 11: Automated Email Reminder Workflow
# ============================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_bg(s11, LIGHT_BG)
add_header(s11, "Automated Email Notification Engine")

mail_img = os.path.join(SCREENSHOT_DIR, "09_sample_reminder_email.png")
if os.path.exists(mail_img):
    s11.shapes.add_picture(mail_img, Inches(0.8), Inches(1.8), Inches(6.2), Inches(4.8))

add_card(s11, Inches(7.3), Inches(1.8), Inches(5.2), Inches(4.8),
         "Notification Engine Architecture", [
    "Trigger Mechanism: Runs at startup and daily at 08:00 AM via APScheduler.",
    "Assignment Policy: Triggers when due_date = tomorrow AND status != 'Completed'.",
    "Exam Policy: Two-stage reminder dispatched at 3 days before AND 1 day before.",
    "Deduplication: Queries notification_log before sending; prevents repeat emails.",
    "Resilient Fallback: If SMTP credentials are unset, logs nicely formatted email to console.",
    "Demo Mode: Instant trigger button on Settings page + 1-minute interval setting."
])

# ============================================================
# SLIDE 12: Challenges Faced & Engineering Solutions
# ============================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_bg(s12, LIGHT_BG)
add_header(s12, "Engineering Challenges & Solutions")

add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "macOS Port 5000 AirPlay Conflict", [
    "Challenge: macOS Monterey & later reserve ports 5000 & 7000 for AirPlay Receiver.",
    "Symptom: Flask default port 5000 fails silently or throws 'Address already in use'.",
    "Resolution: Configured host port 8085 (APP_PORT) and DB port 3307 (DB_HOST_PORT).",
    "Best Practice: Fully parameterized in .env; verified using 'lsof -i :8085'."
])

add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "Database Readiness & Startup Race Condition", [
    "Challenge: MySQL takes 15-25 seconds to initialize; Flask crashes if it connects immediately.",
    "Resolution 1: Docker healthcheck on MySQL (mysqladmin ping) + depends_on service_healthy.",
    "Resolution 2: Resilient retry loop in db.py (10 retries, 3s delay) inside Python app.",
    "Resolution 3: Gunicorn --preload with post_fork hook ensures scheduler starts exactly once."
])

# ============================================================
# SLIDE 13: Cloud Computing Concepts Demonstrated
# ============================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_bg(s13, LIGHT_BG)
add_header(s13, "Cloud Computing Principles Demonstrated")

add_card(s13, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
         "Containerization & Portability", [
    "Encapsulated Runtime: All dependencies bundled inside Docker container images.",
    "'Works on My Machine' Solved: Identical execution across macOS, Linux, and Windows.",
    "Architecture Agnostic: Runs seamlessly on Apple Silicon (ARM64) and Intel (x86_64).",
    "Immutable Infrastructure: Base image builds provide reproducible test environments."
])

add_card(s13, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
         "Networking & Storage", [
    "Software-Defined Network: Isolated user-defined bridge network (studytrack-network).",
    "Container DNS Resolution: Web accesses database by service name 'db' rather than IP.",
    "Volume Decoupling: Data lives outside container lifecycle in studytrack-db-data.",
    "Zero-Data Loss: Containers can be destroyed and rebuilt while student records persist."
])

add_card(s13, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
         "Observability & Health Checks", [
    "Active Probing: Native /health HTTP endpoint inspects DB socket connectivity.",
    "Self-Healing: Restart policy 'unless-stopped' automatically recovers crashed containers.",
    "Structured Logging: Centralized stdout/stderr logging accessible via docker logs.",
    "Microservice Ready: Both tiers communicate over standard network protocols."
])

# ============================================================
# SLIDE 14: Automated CI/CD Pipeline & Quality Assurance
# ============================================================
s_ci = prs.slides.add_slide(blank_layout)
set_slide_bg(s_ci, LIGHT_BG)
add_header(s_ci, "DevOps Automation: GitHub Actions CI/CD Pipeline")

test_img = os.path.join(SCREENSHOT_DIR, "14_automated_tests_pass.png")
if os.path.exists(test_img):
    s_ci.shapes.add_picture(test_img, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.8))

add_card(s_ci, Inches(7.9), Inches(1.8), Inches(4.6), Inches(4.8),
         "CI/CD Pipeline Stages", [
    "Stage 1 - Unit Tests: 12 automated test cases covering auth hashing, template math, and routes.",
    "Stage 2 - Multi-Tier Integration: GitHub Actions executes 'docker compose up -d' in cloud runner.",
    "Active Health Probe: Polls /health endpoint and executes SQL queries inside MySQL container.",
    "Zero-Regression Guarantee: Tests execute in ephemeral clean environments on every git push.",
    "CD-Ready: Builds production multi-arch Docker image with Buildx layer caching."
])

# ============================================================
# SLIDE 15: Future Scope & Cloud Deployment
# ============================================================
s14 = prs.slides.add_slide(blank_layout)
set_slide_bg(s14, LIGHT_BG)
add_header(s14, "Future Scope & Production Cloud Roadmap")

add_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "Cloud Migration Architecture", [
    "AWS Deployment: Deploy Flask web container to AWS ECS (Fargate) behind an Application Load Balancer.",
    "Managed Database: Migrate MySQL container to AWS RDS (Multi-AZ MySQL) for automatic backups.",
    "Secret Management: Store SMTP passwords and session keys in AWS Secrets Manager.",
    "Elastic Scalability: Auto-scale web containers dynamically based on CPU/traffic spikes."
])

add_card(s14, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
         "Advanced Feature Roadmap", [
    "CI/CD Pipeline: Automated testing, image building, and deployment via GitHub Actions.",
    "Redis Caching Layer: Cache dashboard metrics to reduce database query load.",
    "Multi-Channel Alerts: Integrate Twilio SMS and Firebase Cloud Messaging (FCM) mobile push.",
    "Calendar Synchronization: Export deadlines to Google Calendar and Apple iCal via .ics feeds."
])

# ============================================================
# SLIDE 15: Conclusion & Q&A
# ============================================================
s15 = prs.slides.add_slide(blank_layout)
set_slide_bg(s15, NAVY)

c_box = s15.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.0))
tfc = c_box.text_frame
tfc.word_wrap = True

pc1 = tfc.paragraphs[0]
pc1.text = "CONCLUSION & DEMONSTRATION"
pc1.font.size = Pt(14)
pc1.font.bold = True
pc1.font.color.rgb = TEAL

pc2 = tfc.add_paragraph()
pc2.text = "StudyTrack Successfully Implements a Robust, Cloud-Native Two-Tier Architecture"
pc2.font.size = Pt(28)
pc2.font.bold = True
pc2.font.color.rgb = WHITE
pc2.space_after = Pt(20)

points = [
    "Delivered a complete, beginner-friendly student utility far beyond basic tutorials.",
    "Demonstrated core cloud concepts: containerization, custom bridge networks, volumes, and healthchecks.",
    "Solved real development hurdles including macOS port conflicts and database startup sync.",
    "Stack is live at http://localhost:8085 with 100% verified test cases and data persistence."
]
for pt in points:
    p = tfc.add_paragraph()
    p.text = "✔  " + pt
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(220, 225, 245)
    p.space_after = Pt(8)

p_qa = tfc.add_paragraph()
p_qa.text = "\nThank You! Open for Questions & Live Demonstration."
p_qa.font.size = Pt(20)
p_qa.font.bold = True
p_qa.font.color.rgb = ACCENT_ORANGE

output_path = os.path.join(os.path.dirname(__file__), "docs", "StudyTrack_Presentation.pptx")
prs.save(output_path)
print(f"Presentation saved successfully to: {output_path}")
