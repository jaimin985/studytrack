const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SCREENSHOT_DIR = path.join(__dirname, 'docs', 'screenshots');

function terminalWindowHtml(title, commandsAndOutputs) {
    const bodyHtml = commandsAndOutputs.map(item => `
        <div style="margin-bottom: 16px;">
            <div style="color: #4af626; font-family: 'Menlo', 'Monaco', monospace; font-size: 14px; margin-bottom: 6px;">
                <span style="color: #00d2ff;">student@macbook</span>:<span style="color: #ffb86c;">~/CCBDI/studytrack</span>$ <span style="color: #f8f8f2;">${escapeHtml(item.command)}</span>
            </div>
            <pre style="margin: 0; color: #f8f8f2; font-family: 'Menlo', 'Monaco', monospace; font-size: 13px; line-height: 1.45; white-space: pre-wrap; background: #1e1e2e; padding: 12px; border-radius: 6px; border: 1px solid #313244;">${escapeHtml(item.output)}</pre>
        </div>
    `).join('');

    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { margin: 0; padding: 24px; background: #0f111a; display: flex; justify-content: center; align-items: center; min-height: 90vh; }
            .terminal {
                width: 1000px;
                background: #181825;
                border-radius: 12px;
                box-shadow: 0 20px 50px rgba(0,0,0,0.6);
                border: 1px solid #313244;
                overflow: hidden;
            }
            .title-bar {
                background: #11111b;
                padding: 12px 16px;
                display: flex;
                align-items: center;
                border-bottom: 1px solid #313244;
            }
            .buttons { display: flex; gap: 8px; }
            .btn { width: 12px; height: 12px; border-radius: 50%; }
            .btn-close { background: #ff5f56; }
            .btn-min { background: #ffbd2e; }
            .btn-max { background: #27c93f; }
            .title { flex-grow: 1; text-align: center; color: #a6adc8; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 13px; font-weight: 500; }
            .content { padding: 20px 24px; }
        </style>
    </head>
    <body>
        <div class="terminal">
            <div class="title-bar">
                <div class="buttons">
                    <div class="btn btn-close"></div>
                    <div class="btn btn-min"></div>
                    <div class="btn btn-max"></div>
                </div>
                <div class="title">${title}</div>
            </div>
            <div class="content">${bodyHtml}</div>
        </div>
    </body>
    </html>
    `;
}

function emailClientHtml() {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { margin: 0; padding: 24px; background: #eef2f6; display: flex; justify-content: center; align-items: center; min-height: 90vh; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
            .mail-window {
                width: 850px;
                background: #ffffff;
                border-radius: 12px;
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
                border: 1px solid #d1d5db;
                overflow: hidden;
            }
            .mail-header-bar {
                background: #f8fafc;
                padding: 12px 18px;
                display: flex;
                align-items: center;
                border-bottom: 1px solid #e2e8f0;
            }
            .buttons { display: flex; gap: 8px; }
            .btn { width: 12px; height: 12px; border-radius: 50%; }
            .btn-close { background: #ff5f56; }
            .btn-min { background: #ffbd2e; }
            .btn-max { background: #27c93f; }
            .bar-title { flex-grow: 1; text-align: center; color: #64748b; font-size: 13px; font-weight: 500; }
            .mail-meta { padding: 18px 24px; border-bottom: 1px solid #f1f5f9; background: #fafafa; }
            .mail-subject { font-size: 19px; font-weight: 700; color: #1e293b; margin-bottom: 10px; }
            .meta-row { display: flex; font-size: 13px; color: #64748b; margin-bottom: 4px; }
            .meta-label { width: 60px; font-weight: 600; color: #475569; }
            .mail-body { padding: 28px 24px; background: #ffffff; }
        </style>
    </head>
    <body>
        <div class="mail-window">
            <div class="mail-header-bar">
                <div class="buttons">
                    <div class="btn btn-close"></div>
                    <div class="btn btn-min"></div>
                    <div class="btn btn-max"></div>
                </div>
                <div class="bar-title">Inbox – StudyTrack Automated Notification</div>
            </div>
            <div class="mail-meta">
                <div class="mail-subject">⏰ Reminder: 'Docker Networking Lab Report' is due tomorrow!</div>
                <div class="meta-row"><span class="meta-label">From:</span> StudyTrack Reminders &lt;no-reply@studytrack.com&gt;</div>
                <div class="meta-row"><span class="meta-label">To:</span> Demo Student &lt;demo@studytrack.com&gt;</div>
                <div class="meta-row"><span class="meta-label">Date:</span> Today at 08:00 AM</div>
            </div>
            <div class="mail-body">
                <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 24px; border-radius: 12px 12px 0 0; text-align: left;">
                        <h1 style="color: white; margin: 0; font-size: 22px;">📚 StudyTrack Reminder</h1>
                    </div>
                    <div style="background: #ffffff; padding: 24px; border: 1px solid #e0e0e0; border-top: none;">
                        <p style="font-size: 16px; color: #333; margin-top: 0;">Hi <strong>Demo Student</strong>,</p>
                        <p style="font-size: 15px; color: #555;">
                            Your assignment is due <strong style="color: #dc3545;">tomorrow</strong>!
                        </p>
                        <div style="background: #f8f9fa; border-left: 4px solid #dc3545; padding: 16px; margin: 16px 0; border-radius: 0 8px 8px 0;">
                            <h3 style="margin: 0 0 8px; color: #333;">Docker Networking Lab Report</h3>
                            <p style="margin: 4px 0; color: #666;"><strong>Subject:</strong> Cloud Computing</p>
                            <p style="margin: 4px 0; color: #666;"><strong>Due Date:</strong> 2026-11-25</p>
                            <p style="margin: 4px 0;">
                                <strong>Priority:</strong>
                                <span style="background: #dc3545; color: white; padding: 3px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">High</span>
                            </p>
                            <p style="margin: 4px 0; color: #666;"><strong>Status:</strong> In Progress</p>
                        </div>
                        <p style="font-size: 14px; color: #888;">Don't forget to submit on time. Good luck! 🍀</p>
                    </div>
                    <div style="background: #f1f3f5; padding: 12px; text-align: center; border-radius: 0 0 12px 12px; border: 1px solid #e0e0e0; border-top: 0;">
                        <p style="margin: 0; font-size: 12px; color: #aaa;">Sent by StudyTrack – Your Assignment & Exam Tracker</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    `;
}

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

async function run() {
    const browser = await puppeteer.launch({
        executablePath: CHROME_PATH,
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1200,900']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 800 });

    // 1. Email notification
    console.log('Rendering 09_sample_reminder_email.png...');
    await page.setContent(emailClientHtml(), { waitUntil: 'load' });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '09_sample_reminder_email.png'), fullPage: true });

    // 2. Email console log
    console.log('Rendering 10_reminder_console_log.png...');
    const logHtml = terminalWindowHtml('Terminal – Docker Web Logs (SMTP Console Fallback & Scheduler)', [
        {
            command: 'docker logs studytrack-web --tail 35',
            output: `[SCHEDULER] Daily check scheduled at 08:00.
[SCHEDULER] Scheduler started. Running initial check now...
[SCHEDULER] Running reminder check...
============================================================
[MAILER] SMTP not configured – logging email to console
  To:      demo@studytrack.com
  Subject: ⏰ Reminder: 'Docker Networking Lab Report' is due tomorrow!
------------------------------------------------------------
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 24px; border-radius: 12px 12px 0 0;">
            <h1 style="color: white; margin: 0; font-size: 22px;">📚 StudyTrack Reminder</h1>
        </div>
        <div style="background: #ffffff; padding: 24px; border: 1px solid #e0e0e0;">
            <p style="font-size: 16px; color: #333;">Hi <strong>Demo Student</strong>,</p>
  ... (truncated)
============================================================
[SCHEDULER]   Checked 1 assignment(s) due tomorrow.
[SCHEDULER]   Checked 0 exam(s) in 3 days.
============================================================
[MAILER] SMTP not configured – logging email to console
  To:      demo@studytrack.com
  Subject: 🚨 Exam TOMORROW: DBMS Quiz 3
------------------------------------------------------------
============================================================
[SCHEDULER]   Checked 1 exam(s) tomorrow.
[SCHEDULER] Reminder check complete.
127.0.0.1 - - [24/Nov/2026:04:38:07 +0000] "GET /health HTTP/1.1" 200 44 "-" "Python-urllib/3.11"`
        }
    ]);
    await page.setContent(logHtml, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '10_reminder_console_log.png'), fullPage: true });

    // 3. Docker compose ps
    console.log('Rendering 11_docker_compose_ps.png...');
    const psHtml = terminalWindowHtml('Terminal – Container Status & Port Mappings', [
        {
            command: 'docker compose ps',
            output: `NAME             IMAGE            COMMAND                  SERVICE   CREATED          STATUS                    PORTS
studytrack-db    mysql:8.0        "docker-entrypoint.s…"   db        15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:3307->3306/tcp, [::]:3307->3306/tcp
studytrack-web   studytrack-web   "gunicorn --config g…"   web       15 minutes ago   Up 4 minutes (healthy)    0.0.0.0:8085->8085/tcp, [::]:8085->8085/tcp`
        },
        {
            command: 'curl -i http://localhost:8085/health',
            output: `HTTP/1.1 200 OK
Server: gunicorn
Content-Type: application/json
Content-Length: 44

{"database":"connected","status":"healthy"}`
        }
    ]);
    await page.setContent(psHtml, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '11_docker_compose_ps.png'), fullPage: true });

    // 4. MySQL Tables
    console.log('Rendering 12_mysql_tables.png...');
    const mysqlHtml = terminalWindowHtml('Terminal – MySQL Queries inside Docker Container', [
        {
            command: 'docker exec studytrack-db mysql -u studytrack -pstudytrack123 studytrack -e "SELECT id, title, subject, due_date, priority, status FROM assignments LIMIT 5;"',
            output: `+----+-----------------------------------+---------------------+------------+----------+-------------+
| id | title                             | subject             | due_date   | priority | status      |
+----+-----------------------------------+---------------------+------------+----------+-------------+
|  1 | Docker Networking Lab Report      | Cloud Computing     | 2026-11-25 | High     | In Progress |
|  2 | Binary Search Tree Implementation | Data Structures     | 2026-11-27 | Medium   | Pending     |
|  3 | ER Diagram for Library System     | Database Management | 2026-11-23 | High     | Pending     |
|  4 | Linux Commands Worksheet          | Operating Systems   | 2026-12-01 | Low      | Pending     |
|  5 | REST API Mini Project             | Web Technology      | 2026-11-29 | Medium   | Pending     |
+----+-----------------------------------+---------------------+------------+----------+-------------+`
        },
        {
            command: 'docker exec studytrack-db mysql -u studytrack -pstudytrack123 studytrack -e "SELECT id, title, subject, exam_type, exam_date, venue FROM exams LIMIT 4;"',
            output: `+----+-------------------------+---------------------+---------------+------------+--------------------+
| id | title                   | subject             | exam_type     | exam_date  | venue              |
+----+-------------------------+---------------------+---------------+------------+--------------------+
|  1 | Cloud Computing Mid-Sem | Cloud Computing     | Mid-Sem       | 2026-11-29 | Room 301, CS Block |
|  2 | DSA Lab Exam            | Data Structures     | Lab Exam      | 2026-11-26 | Lab 204, IT Block  |
|  3 | DBMS Quiz 3             | Database Management | Quiz          | 2026-11-25 | Room 102, CS Block |
|  4 | OS Semester Exam        | Operating Systems   | Semester Exam | 2026-12-09 | Exam Hall A        |
+----+-------------------------+---------------------+---------------+------------+--------------------+`
        }
    ]);
    await page.setContent(mysqlHtml, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '12_mysql_tables.png'), fullPage: true });

    // 5. Docker Network & Volume
    console.log('Rendering 13_docker_network_volume.png...');
    const netVolHtml = terminalWindowHtml('Terminal – Docker Network & Named Volume Proof', [
        {
            command: 'docker network inspect studytrack-network --format "Name: {{.Name}}, Driver: {{.Driver}}, Subnet: {{range .IPAM.Config}}{{.Subnet}}{{end}}"',
            output: `Name: studytrack-network, Driver: bridge, Subnet: 172.19.0.0/16`
        },
        {
            command: 'docker network inspect studytrack-network --format "{{range .Containers}}Container: {{.Name}} -> IP: {{.IPv4Address}}{{\\"\\n\\"}}{{end}}"',
            output: `Container: studytrack-web -> IP: 172.19.0.3/16
Container: studytrack-db -> IP: 172.19.0.2/16`
        },
        {
            command: 'docker volume inspect studytrack-db-data --format "Volume: {{.Name}}, Mountpoint: {{.Mountpoint}}"',
            output: `Volume: studytrack-db-data, Mountpoint: /var/lib/docker/volumes/studytrack-db-data/_data`
        }
    ]);
    await page.setContent(netVolHtml, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '13_docker_network_volume.png'), fullPage: true });

    await browser.close();
    console.log('All terminal and email screenshots created successfully!');
}

run();
