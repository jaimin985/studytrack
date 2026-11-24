"""
generate_simulation_docx.py – Converts Simulation_Guide into a clean,
formatted Word document: docs/Simulation_Guide.docx
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = docx.Document()

# Set standard 1 inch margins
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Colors
NAVY = RGBColor(26, 35, 126)
DARK_GRAY = RGBColor(50, 50, 50)
CODE_COLOR = RGBColor(180, 40, 40)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = NAVY
    p.paragraph_format.space_after = Pt(4)

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(12)
    run.font.italic = True
    run.font.color.rgb = RGBColor(100, 100, 100)
    p.paragraph_format.space_after = Pt(18)

def add_h1(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = NAVY
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)

def add_h2(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(63, 81, 181)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)

def add_p(text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = DARK_GRAY
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(11)
    r_text.font.color.rgb = DARK_GRAY

def add_code_block(code_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run(code_text)
    run.font.name = "Courier New"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(30, 30, 30)

def add_quote(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("“ " + text + " ”")
    run.font.name = "Georgia"
    run.font.size = Pt(10.5)
    run.font.italic = True
    run.font.color.rgb = RGBColor(40, 80, 130)

# Build Content
add_title("StudyTrack: Simulation & Lab Demonstration Runbook")
add_subtitle("Cloud Computing Lab • Two-Tier Containerized Application on Docker Desktop (macOS)")

# Summary Table
table = doc.add_table(rows=7, cols=3)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Parameter", "Value", "Operational Note"]
hdr_cells = table.rows[0].cells
for i, h in enumerate(headers):
    hdr_cells[i].text = h
    set_cell_background(hdr_cells[i], "1A237E")
    for r in hdr_cells[i].paragraphs[0].runs:
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

data = [
    ("Web Application URL", "http://localhost:8085", "Never use 5000 (macOS AirPlay collision)"),
    ("MySQL Host Port", "3307", "Host port mapping; internal container port is 3306"),
    ("Demo Credentials", "demo@studytrack.com / Demo@123", "Pre-seeded student account with initial records"),
    ("Health Check Endpoint", "http://localhost:8085/health", "Active DB ping probe used by Docker healthcheck"),
    ("Bridge Network", "studytrack-network", "Private container network (Subnet: 172.19.0.0/16)"),
    ("Persistent Volume", "studytrack-db-data", "Mounts to /var/lib/mysql; outlives container deletion")
]
for row_idx, row_data in enumerate(data, start=1):
    row_cells = table.rows[row_idx].cells
    for col_idx, text in enumerate(row_data):
        row_cells[col_idx].text = text
        bg = "F4F6FB" if row_idx % 2 == 1 else "FFFFFF"
        set_cell_background(row_cells[col_idx], bg)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

add_h1("1. Prerequisites & Environment Verification")
add_h2("Step 1.1: Verify Docker Engine & Compose")
add_p("Ensure Docker Desktop is running and command-line tools are accessible.", "What to do: ")
add_code_block("docker --version && docker compose version")
add_p("Docker version 27.x.x / Compose v2.x.x confirmed.", "Expected Result: ")
add_quote("We have verified that Docker Desktop is actively running on our macOS host machine, providing native container orchestration via Docker Compose v2.")

add_h2("Step 1.2: Host Port Conflict Verification (macOS Port 5000 / 8085 Rule)")
add_p("Confirm that host port 8085 is free and not claimed by macOS AirPlay.", "What to do: ")
add_code_block("lsof -i :8085")
add_p("No output returned (port 8085 is completely open).", "Expected Result: ")
add_quote("By default, Flask tutorials use port 5000. However, on macOS Monterey and later, port 5000 is occupied by AirPlay Receiver. We explicitly configured host port 8085 in .env to eliminate port collisions.")

add_h1("2. Configuration & Launching the Stack")
add_h2("Step 2.1: Verify Environment Configuration")
add_code_block("cp .env.example .env\ncat .env")
add_p("All secrets, database credentials, and port mappings are externalized into .env and ignored by Git.", "Architecture Note: ")

add_h2("Step 2.2: Build and Start Containers")
add_code_block("docker compose up --build -d")
add_p("Docker builds Python 3.11-slim image, starts MySQL 8.0, and establishes custom bridge network.", "Expected Result: ")
add_quote("Docker Compose initializes our two-tier stack in dependency order. The web service waits until MySQL passes its internal healthcheck before launching Gunicorn.")

add_h2("Step 2.3: Verify Container Health & Connectivity")
add_code_block("docker compose ps\ncurl -i http://localhost:8085/health")
add_p("Both containers report 'Up (healthy)'. The /health endpoint returns HTTP 200 with {'database':'connected','status':'healthy'}.", "Expected Result: ")

add_h1("3. Step-by-Step Live Demonstration Script")
add_p("1. Review Login Screen: Open http://localhost:8085/login. Note the modern responsive card layout.", "Step 1: ")
add_p("2. Register New Student: Navigate to /register. Create an account for Alex Kumar (alex@college.edu). Highlights strict tenant data isolation.", "Step 2: ")
add_p("3. Log in as Demo Student: Access pre-seeded records via demo@studytrack.com / Demo@123.", "Step 3: ")
add_p("4. Walk Through Dashboard: Showcase summary metrics (Pending, Due This Week, Overdue, Completed), completion progress bar, deadline countdown badges, and upcoming exams.", "Step 4: ")
add_p("5. Add Assignment: Click 'Add Assignment' modal. Set title 'Cloud Architecture Study', priority 'High', due tomorrow. Observes instant red countdown pill.", "Step 5: ")
add_p("6. Add Exam: Schedule 'Cloud Computing Lab Exam' for tomorrow in Room 301.", "Step 6: ")
add_p("7. Test Filtering & Search: Filter by 'High' priority, 'In Progress' status, and search keywords dynamically.", "Step 7: ")
add_p("8. Trigger Reminder Engine: On /settings, click 'Run Reminder Check Now'. Inspect console logs (docker logs studytrack-web) to witness APScheduler scanning, building HTML email, and deduplicating in notification_log.", "Step 8: ")

add_h1("4. Proving Two-Tier Cloud Concepts to Evaluators")
add_h2("Proof A: Container Network Isolation")
add_code_block("docker network inspect studytrack-network")
add_quote("Both containers belong to 'studytrack-network'. Web communicates with MySQL using container DNS (db:3306), isolated from the public network.")

add_h2("Proof B: Direct SQL Verification inside Container")
add_code_block("docker exec studytrack-db mysql -u studytrack -pstudytrack123 studytrack -e 'SELECT * FROM assignments LIMIT 5;'")
add_quote("This query runs directly inside the database container, proving real relational persistence with foreign keys.")

add_h2("Proof C: Volume Data Persistence Across Destruction")
add_code_block("docker compose down\ndocker compose up -d\ndocker exec studytrack-db mysql -u studytrack -pstudytrack123 studytrack -e 'SELECT count(*) FROM assignments;'")
add_quote("Even after tearing down both containers, our assignment count remains completely intact because persistent storage is offloaded to the named volume studytrack-db-data.")

add_h2("Proof D: Automated CI/CD Test Suite Execution")
add_code_block("docker exec studytrack-web python -m unittest discover -s /app/tests -v")
add_quote("All 12 automated unit and integration tests execute inside the container, achieving 100% test pass rate across auth, mailer, and route endpoints before deployment.")

add_h1("5. Common Viva Questions & Answers")
add_p("Q: What makes this a two-tier architecture? A: Tier 1 (Flask + Gunicorn) handles business logic and presentation; Tier 2 (MySQL 8.0) handles relational data storage. Containers run on separate lifecycles and scale independently.")
add_p("Q: Why was host port 8085 selected? A: macOS Monterey+ binds AirPlay Receiver to port 5000. Port 8085 avoids conflicts completely.")
add_p("Q: How does the email reminder system handle missing credentials? A: If SMTP credentials are not configured, the system logs the rendered HTML email to standard output so development and faculty demos never crash.")
add_p("Q: How would you deploy this to AWS? A: Containerize with Amazon ECR, deploy web containers on AWS ECS Fargate behind an Application Load Balancer, and migrate database storage to AWS RDS Multi-AZ MySQL.")

output_path = os.path.join(os.path.dirname(__file__), "docs", "Simulation_Guide.docx")
doc.save(output_path)
print(f"Simulation Guide DOCX saved successfully to: {output_path}")
