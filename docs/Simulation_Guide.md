# StudyTrack: Simulation & Lab Demonstration Runbook

**Course:** Cloud Computing Laboratory  
**Project:** StudyTrack – Student Assignment & Exam Tracker (Two-Tier Architecture)  
**Target Environment:** macOS (Apple Silicon / Intel) with Docker Desktop  
**Document Purpose:** A complete, step-by-step reproduction guide and live demonstration script for students and evaluating faculty.

---

## Quick Reference Summary

| Parameter | Value | Note |
|---|---|---|
| **Web Application URL** | `http://localhost:8085` | **Never port 5000** (AirPlay conflict on macOS) |
| **MySQL Host Port** | `3307` | Host mapping; internal container port is `3306` |
| **Pre-Seeded Demo Account** | `demo@studytrack.com` | Password: `Demo@123` |
| **Health Check Endpoint** | `http://localhost:8085/health` | Returns JSON status of Web & DB connectivity |
| **Bridge Network Name** | `studytrack-network` | Private container network (Subnet `172.19.0.0/16`) |
| **Persistent Named Volume** | `studytrack-db-data` | Mounts to `/var/lib/mysql` inside database container |

---

## 1. System Prerequisites & Verification

Before running StudyTrack, ensure your host environment meets the prerequisites.

### Step 1.1: Verify Docker Engine & Docker Compose
* **What to do:** Open macOS Terminal and ensure Docker Desktop is running and the command-line tools are accessible.
* **Exact Command:**
  ```bash
  docker --version && docker compose version
  ```
* **Expected Result:**
  ```text
  Docker version 27.x.x (or newer), build ...
  Docker Compose version v2.x.x (or newer)
  ```
* **What to tell the professor:**
  > *"We have verified that Docker Desktop is running on our host machine. Docker Compose version 2 is bundled natively, providing container lifecycle management and multi-container orchestration."*

### Step 1.2: Check Host Port Availability (macOS Port 5000 / 8085 Rule)
* **What to do:** Confirm that host port `8085` is free and not claimed by another process.
* **Exact Command:**
  ```bash
  lsof -i :8085
  ```
* **Expected Result:** Command returns blank (no output), indicating port 8085 is completely open.
* **What to tell the professor:**
  > *"By default, Flask tutorials use port 5000. However, on macOS Monterey, Ventura, and Sonoma, port 5000 is reserved by macOS AirPlay Receiver (`ControlCenter`). We deliberately re-engineered our host port mapping to port 8085 in `.env` to prevent silent port collision."*

---

## 2. Project Setup & Environment Configuration

### Step 2.1: Navigate to Project Directory
* **What to do:** Open your shell and change directory to the project root.
* **Exact Command:**
  ```bash
  cd /Users/jaimindudhat/Downloads/CCBDI/studytrack
  ls -la
  ```
* **Expected Result:** Directory listing showing `app/`, `db/`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `.env.example`, `.env`, and `docs/`.
* **What to tell the professor:**
  > *"The repository follows standard cloud-native structure: isolated application code, standalone database scripts, explicit container manifests, and environment templates."*

### Step 2.2: Configure the Environment Variables (.env)
* **What to do:** Verify or copy `.env.example` to `.env`.
* **Exact Command:**
  ```bash
  cp .env.example .env
  cat .env
  ```
* **Expected Result:**
  ```text
  APP_PORT=8085
  SECRET_KEY=dev-secret-key-change-in-production
  MYSQL_HOST=db
  MYSQL_PORT=3306
  MYSQL_USER=studytrack
  MYSQL_PASSWORD=studytrack123
  MYSQL_DATABASE=studytrack
  MYSQL_ROOT_PASSWORD=rootpass123
  DB_HOST_PORT=3307
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USERNAME=
  SMTP_PASSWORD=
  SMTP_FROM_NAME=StudyTrack Reminders
  REMINDER_HOUR=8
  REMINDER_MINUTE=0
  REMINDER_CHECK_INTERVAL_MINUTES=
  ```
* **What to tell the professor:**
  > *"All secrets and environment variables are externalized into `.env` and kept out of version control via `.gitignore`. Docker Compose injects these variables into the container environment at runtime."*

### Step 2.3: Optional Gmail SMTP App Password Configuration
* **What to do:** If real email delivery to an inbox is desired during testing:
  1. Go to [Google Account Security](https://myaccount.google.com/security) and ensure **2-Step Verification** is ON.
  2. Visit [Google App Passwords](https://myaccount.google.com/apppasswords).
  3. Generate an App Password for **Mail** named `StudyTrack`.
  4. Paste your email address into `SMTP_USERNAME` and the 16-character generated password into `SMTP_PASSWORD` in `.env`.
* **Note:** If SMTP is left empty, **the application will not crash**. It automatically logs the rendered HTML notification to stdout in the container logs.

---

## 3. Building and Starting the Application Stack

### Step 3.1: Build and Launch Containers
* **What to do:** Build the Flask image and start both the Web and Database containers in detached mode.
* **Exact Command:**
  ```bash
  docker compose up --build -d
  ```
* **Expected Result:**
  ```text
  ✔ Network studytrack-network Created
  ✔ Volume studytrack-db-data  Created
  ✔ Container studytrack-db    Healthy
  ✔ Container studytrack-web   Started
  ```
* **What to tell the professor:**
  > *"Docker Compose builds our Python 3.11-slim container image from the Dockerfile, pulls MySQL 8.0, configures the custom bridge network `studytrack-network`, allocates the persistent volume `studytrack-db-data`, and boots the containers in dependency order."*

### Step 3.2: Verify Container Health & Status
* **What to do:** Check that both containers are running and healthy.
* **Exact Command:**
  ```bash
  docker compose ps
  ```
* **Expected Result:**
  ```text
  NAME             IMAGE            COMMAND                  SERVICE   STATUS                    PORTS
  studytrack-db    mysql:8.0        "docker-entrypoint.s…"   db        Up (healthy)              0.0.0.0:3307->3306/tcp
  studytrack-web   studytrack-web   "gunicorn --config g…"   web       Up (healthy)              0.0.0.0:8085->8085/tcp
  ```
* **What to tell the professor:**
  > *"Both containers report `(healthy)`. The web tier relies on Docker's healthcheck mechanism (`depends_on: condition: service_healthy`) to wait until MySQL is completely ready to accept connections before launching Gunicorn."*

### Step 3.3: Execute System Healthcheck Probe
* **What to do:** Query the web tier health endpoint via curl.
* **Exact Command:**
  ```bash
  curl -i http://localhost:8085/health
  ```
* **Expected Result:**
  ```text
  HTTP/1.1 200 OK
  Content-Type: application/json

  {"database":"connected","status":"healthy"}
  ```
* **What to tell the professor:**
  > *"The `/health` endpoint executes an active TCP and SQL handshake to the MySQL container on the bridge network. A 200 OK guarantees end-to-end multi-tier communication is functional."*

---

## 4. Live Faculty Demonstration Script (Step-by-Step)

Follow this chronological demonstration path during the lab examination or viva.

### Step 4.1: Access Application & Review Login Screen
* **Action:** Open your browser and navigate to `http://localhost:8085/login`.
* **Demonstration Points:**
  - Show the modern, responsive card layout with Bootstrap 5 and Bootstrap Icons.
  - Note the pre-seeded demo user credentials indicated on the card: `demo@studytrack.com` / `Demo@123`.
* **What to tell the professor:**
  > *"The login page is styled with a custom gradient theme. Authentication is session-based, and passwords are protected using Werkzeug's modern scrypt key derivation function."*

### Step 4.2: Register a New Student Account
* **Action:** Click **"Register here"** or navigate to `http://localhost:8085/register`.
  - Enter Name: `Alex Kumar`
  - Enter Email: `alex@college.edu`
  - Enter Password: `Password@123`
  - Click **Register**.
* **Expected Result:** Redirects to `/login` with flash message: *"Registration successful! Please log in."*
* **What to tell the professor:**
  > *"Notice that each student account is completely isolated. Data submitted by Alex Kumar will never leak into other students' views due to SQL tenant scoping by `user_id`."*

### Step 4.3: Log in as Demo Student
* **Action:** Log in with:
  - Email: `demo@studytrack.com`
  - Password: `Demo@123`
* **Expected Result:** User is redirected to `/` (Dashboard) with welcome banner *"Welcome back, Demo Student!"*.

### Step 4.4: Walk Through the Dashboard
* **Action:** Walk the professor through the components on the dashboard:
  1. **Top Summary Cards:** Shows instant tallies for *Pending*, *Due This Week*, *Overdue*, and *Completed*.
  2. **Interactive Progress Bar:** Dynamically calculates assignment completion percentage (e.g. `17%` or `33%`).
  3. **Upcoming Deadlines Panel:** Assignments sorted chronologically with dynamic countdown pills:
     - **Red badge:** Due tomorrow or overdue (urgent)
     - **Orange badge:** Due in ≤3 days
     - **Green badge:** Due in >3 days
  4. **Upcoming Exams Panel:** Displays exams with type tags (*Quiz*, *Lab Exam*, *Mid-Sem*, *Semester Exam*), venue, and countdown.

### Step 4.5: Add an Assignment Due Tomorrow
* **Action:**
  1. Click **"New Assignment"** in the top navigation or navigate to `/assignments`.
  2. Click **"Add Assignment"** modal button.
  3. Enter:
     - Title: `Cloud Architecture Case Study`
     - Subject: `Cloud Computing`
     - Description: `Analyze AWS vs Azure two-tier architecture deployments.`
     - Due Date: Set to **Tomorrow's Date**.
     - Priority: `High`
     - Status: `Pending`
  4. Click **Save**.
* **Expected Result:** Assignment is created instantly and appears at the top of the assignments list with a red *"1 day left"* badge.

### Step 4.6: Add an Upcoming Exam
* **Action:**
  1. Navigate to **Exams** tab in the sidebar (`/exams`).
  2. Click **"Add Exam"** button.
  3. Enter:
     - Title: `Cloud Computing Final Practical`
     - Subject: `Cloud Computing`
     - Exam Type: `Lab Exam`
     - Exam Date: Set to **Tomorrow's Date** or **3 Days Ahead**.
     - Exam Time: `14:00`
     - Syllabus: `Dockerfiles, Compose, Docker Networks, Volumes`
     - Venue: `Lab 305, IT Block`
  4. Click **Save**.
* **Expected Result:** Exam card is displayed with green `Lab Exam` badge and countdown.

### Step 4.7: Demonstrate Filtering, Sorting, and Search
* **Action:**
  - On `/assignments`:
    - Select **Priority:** `High` -> Click **Filter** (only high-priority assignments display).
    - Select **Status:** `Completed` -> Click **Filter** (completed history displayed).
    - Sort By: `Priority First` -> High-priority tasks bubble to the top.
    - Type `Docker` in the Search bar -> Filters to Docker-related assignments.
* **What to tell the professor:**
  > *"All filtering and sorting is handled dynamically via parameterized SQL queries with full protection against SQL injection."*

### Step 4.8: Demonstrate Email Notification & Reminder Automation
* **Action:**
  1. Click **Settings** in the sidebar (`/settings`).
  2. Show the **Email Notifications** status card: explains the 1-day assignment deadline rule and 3-day/1-day exam alert rule.
  3. Click **"Run Reminder Check Now"** button.
  4. Switch to Terminal and run:
     ```bash
     docker logs studytrack-web --tail 30
     ```
* **Expected Result:** Terminal displays the executed reminder check:
  ```text
  [SCHEDULER] Running reminder check...
  [MAILER] SMTP not configured – logging email to console
    To:      demo@studytrack.com
    Subject: ⏰ Reminder: 'Cloud Architecture Case Study' is due tomorrow!
  ------------------------------------------------------------
  [SCHEDULER]   Checked 2 assignment(s) due tomorrow.
  [SCHEDULER]   Checked 1 exam(s) tomorrow.
  [SCHEDULER] Reminder check complete.
  ```
* **What to tell the professor:**
  > *"Our notification engine is powered by APScheduler running inside the Gunicorn worker. Notice that it scanned all active assignments and exams, detected the items due tomorrow, composed a styled HTML email, and safely logged it to stdout. The `notification_log` table prevents sending duplicate reminders if the check runs again."*

---

## 5. Proving the Two-Tier Architecture & Cloud Concepts

Run these commands in front of the evaluator to demonstrate cloud architectural depth.

### Step 5.1: Inspect the Isolated Container Bridge Network
* **Command:**
  ```bash
  docker network inspect studytrack-network
  ```
* **Expected Result:** JSON output showing two containers attached:
  - `studytrack-web` with IP `172.19.0.3/16`
  - `studytrack-db` with IP `172.19.0.2/16`
* **What to tell the professor:**
  > *"Both containers belong to `studytrack-network`, an isolated software-defined bridge network. The Flask app connects to the database via internal Docker DNS using the hostname `db` on port 3306. The database is not exposed to the public internet."*

### Step 5.2: Query the Database from Inside the Container
* **Command:**
  ```bash
  docker exec studytrack-db mysql -u studytrack -pstudytrack123 studytrack -e "SELECT id, title, subject, due_date, priority, status FROM assignments LIMIT 5;"
  ```
* **Expected Result:** Formatted ASCII table showing records stored inside MySQL.
* **What to tell the professor:**
  > *"We execute queries directly against the MySQL engine inside the Tier 2 container. This proves data is stored in a relational schema with foreign key constraints, not in memory or local flat files."*

### Step 5.3: Prove Notification Deduplication
* **Command:**
  ```bash
  docker exec studytrack-db mysql -u studytrack -pstudytrack123 studytrack -e "SELECT * FROM notification_log;"
  ```
* **Expected Result:** Shows logged reminders with `user_id`, `item_type`, `item_id`, and `days_before`.
* **What to tell the professor:**
  > *"The `notification_log` table enforces a composite unique constraint `(user_id, item_type, item_id, days_before)`. If the scheduler fires 10 times today, the student receives exactly one notification."*

### Step 5.4: Prove Data Persistence Across Container Destruction
* **Command:**
  ```bash
  # Step A: Stop and remove containers (preserving volumes)
  docker compose down

  # Step B: Restart the stack
  docker compose up -d

  # Step C: Re-query database
  docker exec studytrack-db mysql -u studytrack -pstudytrack123 studytrack -e "SELECT count(*) AS total_assignments FROM assignments;"
  ```
* **Expected Result:** The count remains identical (e.g. `7` assignments). No records were lost.
* **What to tell the professor:**
  > *"We ran `docker compose down`, which terminated and destroyed both containers. When we started them back up with `docker compose up -d`, our new assignments and user accounts remained intact because storage is decoupled into the persistent named volume `studytrack-db-data`."*

### Step 5.5: Run Automated CI/CD Unit & Integration Test Suite
* **Command:**
  ```bash
  docker cp tests studytrack-web:/app/tests
  docker exec studytrack-web python -m unittest discover -s /app/tests -v
  ```
* **Expected Result:**
  ```text
  test_countdown_days_left ... ok
  test_progress_bar_percentage ... ok
  test_dashboard_requires_login ... ok
  test_health_endpoint_healthy ... ok
  test_health_endpoint_unhealthy ... ok
  test_login_page_renders_ok ... ok
  test_register_page_renders_ok ... ok
  test_assignment_email_html_content ... ok
  test_exam_email_html_content ... ok
  test_smtp_not_configured_fallback ... ok
  test_password_hash_uniqueness ... ok
  test_password_hashing_and_verification ... ok

  Ran 12 tests in 0.411s
  OK
  ```
* **What to tell the professor:**
  > *"We implemented a complete CI/CD testing pipeline using GitHub Actions (`.github/workflows/ci-cd.yml`). All 12 automated unit and integration tests run inside the container to validate password security, HTML email rendering, date countdown logic, and the `/health` endpoint before any production release."*

---

## 6. Stack Teardown & Reset Commands

| Objective | Command | Result |
|---|---|---|
| **Stop Stack (Keep Data)** | `docker compose down` | Stops and removes containers and network. Volume and data preserved. |
| **Clean Reset (Wipe All Data)** | `docker compose down -v` | Deletes containers, network, AND named volume `studytrack-db-data`. On next start, `init.sql` will re-seed fresh demo data. |
| **Rebuild Container Image** | `docker compose up --build -d` | Recompiles Python Docker image if code changes were made. |
| **View Live Container Logs** | `docker compose logs -f web` | Streams web application logs, HTTP requests, and scheduler activity. |

---

## 7. Troubleshooting & Common Pitfalls

| Symptom | Cause | Solution |
|---|---|---|
| **`bind: address already in use` on port 5000** | macOS AirPlay Receiver reserves port 5000. | Ensure `APP_PORT=8085` in `.env`. Check with `lsof -i :5000` or disable AirPlay Receiver in *System Settings > General > AirDrop & AirPlay*. |
| **Port 8085 is also busy** | Another local service or previous run using port 8085. | Run `lsof -i :8085` to locate the PID. Either kill the process (`kill -9 <PID>`) or set `APP_PORT=8086` in `.env` and restart. |
| **MySQL container fails with access denied** | Password mismatch in existing volume. | Run `docker compose down -v` to delete old database volumes, then restart with `docker compose up -d`. |
| **Email reminders not arriving in Gmail inbox** | Google account requires 2-Step Verification and an App Password. | Regular account passwords will be rejected. Generate a 16-character App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords). |
| **Flask displays "Database connection failed"** | Race condition if MySQL takes >30s to boot. | Our `db.py` contains a 10-retry loop with 3s backoff, and `docker-compose.yml` uses `service_healthy`. Run `docker compose logs db` to inspect MySQL boot logs. |

---

## 8. Expected Viva & Examination Questions (With High-Scoring Answers)

### Q1: What makes StudyTrack a "Two-Tier" architecture rather than a monolithic or microservice app?
> **Answer:** *"A two-tier architecture divides the application into two distinct layers: the Presentation/Logic Tier (Tier 1 – Flask web application with Gunicorn) and the Persistence Tier (Tier 2 – MySQL 8.0 database). Unlike a single monolith where SQLite or flat files live in the same container as the app, our database runs as an autonomous container on an isolated network. Unlike microservices, which decompose logic into dozens of independent services communicating via REST/gRPC, StudyTrack consolidates business logic in the app tier while decoupling persistent state."*

### Q2: Why did we use host port 8085 instead of the standard Flask port 5000?
> **Answer:** *"Starting in macOS Monterey, Apple enabled AirPlay Receiver by default, which binds to host ports 5000 and 7000 (`ControlCenter`). If a Docker container binds to 5000:5000, macOS either rejects the bind or silently intercepts incoming traffic, preventing the developer from accessing the web app. We solved this by mapping internal container port 8085 to host port 8085 via `.env`."*

### Q3: How do Docker networks provide security in this setup?
> **Answer:** *"We defined a custom bridge network called `studytrack-network`. Within this network, containers discover each other via automatic DNS resolution using service names (`db` and `web`). The database port 3306 is not required to be published to the host for the app to function; it is only exposed on port 3307 for optional administrative inspection. Outside attackers cannot directly access port 3306 on the private bridge."*

### Q4: What is the difference between `docker compose down` and `docker compose down -v`?
> **Answer:** *"`docker compose down` stops and destroys the containers and bridge network, but leaves named volumes untouched. This allows data to persist across container upgrades. Adding the `-v` flag explicitly instructs Docker to delete attached named volumes (`studytrack-db-data`), resulting in a complete factory reset where subsequent starts re-execute `init.sql`."*

### Q5: How would you scale and deploy this architecture to Amazon Web Services (AWS)?
> **Answer:** *"To deploy StudyTrack to AWS production:*
> 1. *Push the Docker image to Amazon Elastic Container Registry (ECR).*
> 2. *Run the Flask container on AWS Elastic Container Service (ECS) using AWS Fargate (serverless containers) behind an Application Load Balancer (ALB).*
> 3. *Replace the MySQL container with Amazon RDS for MySQL (Multi-AZ deployment) for managed automated backups, failover, and encryption at rest.*
> 4. *Store database credentials and SMTP keys securely in AWS Secrets Manager.*
> 5. *Use Amazon Simple Email Service (SES) instead of Gmail SMTP for high-deliverability notification delivery."*
