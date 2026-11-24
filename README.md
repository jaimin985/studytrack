# StudyTrack – Student Assignment & Exam Tracker

> **Cloud Computing Laboratory Project**  
> A containerized, beginner-friendly, two-tier web application built with **Flask (Tier 1)** and **MySQL 8.0 (Tier 2)** orchestrated via **Docker & Docker Compose**.

---

## Quick Start in 5 Commands

```bash
# 1. Clone or navigate to the project directory
cd studytrack

# 2. Create your environment file from the template
cp .env.example .env

# 3. Build and launch the container stack in detached mode
docker compose up --build -d

# 4. Verify system health and container status
curl -i http://localhost:8085/health
docker compose ps

# 5. Open in your browser
open http://localhost:8085
```

---

## Important macOS Port Rule
- **Never use host port 5000 or 7000 on macOS.** macOS Monterey, Ventura, Sonoma, and Sequoia reserve these ports for **AirPlay Receiver** (`ControlCenter`).
- StudyTrack maps host port **8085** (`APP_PORT=8085`) to the web container, and host port **3307** (`DB_HOST_PORT=3307`) to MySQL.
- Verify port availability: `lsof -i :8085`.

---

## Default Access & Demo Account
- **Web Interface:** [http://localhost:8085](http://localhost:8085)
- **Pre-Seeded Demo Account:**
  - **Email:** `demo@studytrack.com`
  - **Password:** `Demo@123`
- **Health Check Endpoint:** [http://localhost:8085/health](http://localhost:8085/health)

---

## Clean Shutdown & Reset
```bash
# Stop containers (preserves database records in named volume)
docker compose down

# Complete factory reset (deletes containers AND wipes database volume)
docker compose down -v
```

---

## Automated CI/CD Pipeline & Testing
StudyTrack includes an enterprise-grade **GitHub Actions CI/CD pipeline** (`.github/workflows/ci-cd.yml`):
- **Stage 1 (Unit Tests):** Automated execution of 12 unit tests across auth, password hashing, and notification email generation.
- **Stage 2 (Integration Test):** Automated multi-container spin-up, healthcheck verification, active `/health` HTTP probe, and clean teardown.
- **Stage 3 (Docker Build):** Production container image compilation.

Run the test suite locally inside the running container:
```bash
docker exec studytrack-web python -m unittest discover -s /app/tests -v
```

---

## Deliverables in `docs/`
- **Presentation:** `docs/StudyTrack_Presentation.pptx` (15 widescreen slides with shapes and real screenshots)
- **Simulation Guide:** `docs/Simulation_Guide.md` and `docs/Simulation_Guide.docx` (step-by-step viva & demo runbook)
- **Lab Report:** `docs/Lab_Report.docx` (formal 15-25 page academic report with test matrices, captions, and code)
- **Real Screenshots:** `docs/screenshots/` (12 high-resolution UI and terminal captures)
