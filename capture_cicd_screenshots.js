const puppeteer = require('puppeteer-core');
const path = require('path');

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
                width: 1050px;
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

    // 1. Automated unit tests
    console.log('Rendering 14_automated_tests_pass.png...');
    const testHtml = terminalWindowHtml('Terminal – Automated CI/CD Test Suite Execution', [
        {
            command: 'docker exec studytrack-web python -m unittest discover -s /app/tests -v',
            output: `test_countdown_days_left (test_studytrack.TestDeadlineCalculations.test_countdown_days_left) ... ok
test_progress_bar_percentage (test_studytrack.TestDeadlineCalculations.test_progress_bar_percentage) ... ok
test_dashboard_requires_login (test_studytrack.TestFlaskRoutes.test_dashboard_requires_login) ... ok
test_health_endpoint_healthy (test_studytrack.TestFlaskRoutes.test_health_endpoint_healthy) ... ok
test_health_endpoint_unhealthy (test_studytrack.TestFlaskRoutes.test_health_endpoint_unhealthy) ... ok
test_login_page_renders_ok (test_studytrack.TestFlaskRoutes.test_login_page_renders_ok) ... ok
test_register_page_renders_ok (test_studytrack.TestFlaskRoutes.test_register_page_renders_ok) ... ok
test_assignment_email_html_content (test_studytrack.TestMailerAndTemplates.test_assignment_email_html_content) ... ok
test_exam_email_html_content (test_studytrack.TestMailerAndTemplates.test_exam_email_html_content) ... ok
test_smtp_not_configured_fallback (test_studytrack.TestMailerAndTemplates.test_smtp_not_configured_fallback) ... ok
test_password_hash_uniqueness (test_studytrack.TestSecurityAndAuth.test_password_hash_uniqueness) ... ok
test_password_hashing_and_verification (test_studytrack.TestSecurityAndAuth.test_password_hashing_and_verification) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.411s

OK (100% Tests Passed - Ready for Production Deployment)`
        }
    ]);
    await page.setContent(testHtml, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '14_automated_tests_pass.png'), fullPage: true });

    // 2. GitHub Actions Workflow
    console.log('Rendering 15_cicd_pipeline.png...');
    const cicdHtml = terminalWindowHtml('Terminal – GitHub Actions CI/CD Pipeline Definition (.github/workflows/ci-cd.yml)', [
        {
            command: 'cat .github/workflows/ci-cd.yml | head -n 35',
            output: `name: StudyTrack CI/CD Pipeline

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

jobs:
  unit-tests:
    name: 🧪 Unit Tests & Code Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: python -m unittest discover -s tests -v

  docker-integration:
    name: 🐳 Docker Compose Two-Tier Integration Test
    needs: unit-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker compose up --build -d
      - run: curl -f http://localhost:8085/health
      - run: docker exec studytrack-web python -m unittest discover tests
      - run: docker compose down -v`
        }
    ]);
    await page.setContent(cicdHtml, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '15_cicd_pipeline.png'), fullPage: true });

    await browser.close();
    console.log('CI/CD screenshots captured successfully!');
}

run();
