const puppeteer = require('puppeteer-core');
const path = require('path');

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SCREENSHOT_DIR = path.join(__dirname, 'docs', 'screenshots');
const BASE_URL = 'http://localhost:8085';

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function capture() {
    console.log('Launching Chrome from:', CHROME_PATH);
    const browser = await puppeteer.launch({
        executablePath: CHROME_PATH,
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1400,900']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 900 });

    try {
        // 1. Login Page
        console.log('Capturing Login Page...');
        await page.goto(`${BASE_URL}/login`, { waitUntil: 'networkidle0' });
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '01_login.png'), fullPage: false });

        // 2. Register Page
        console.log('Capturing Register Page...');
        await page.goto(`${BASE_URL}/register`, { waitUntil: 'networkidle0' });
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '02_register.png'), fullPage: false });

        // 3. Perform Login
        console.log('Logging in as demo@studytrack.com...');
        await page.goto(`${BASE_URL}/login`, { waitUntil: 'networkidle0' });
        await page.type('input[name="email"]', 'demo@studytrack.com');
        await page.type('input[name="password"]', 'Demo@123');
        await Promise.all([
            page.waitForNavigation({ waitUntil: 'networkidle0' }),
            page.click('button[type="submit"]')
        ]);

        // 4. Dashboard
        console.log('Capturing Dashboard...');
        await sleep(500);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '03_dashboard.png'), fullPage: false });

        // 5. Assignments Page
        console.log('Capturing Assignments Page...');
        await page.goto(`${BASE_URL}/assignments`, { waitUntil: 'networkidle0' });
        await sleep(500);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '04_assignments.png'), fullPage: false });

        // 6. Add Assignment Modal
        console.log('Capturing Add Assignment Modal...');
        await page.click('button[data-bs-target="#addAssignmentModal"]');
        await sleep(600); // wait for Bootstrap modal fade-in
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '05_add_assignment_modal.png'), fullPage: false });
        // Close modal
        await page.click('#addAssignmentModal .btn-close');
        await sleep(500);

        // 7. Filtered Assignments
        console.log('Capturing Filtered Assignments...');
        await page.select('select[name="priority"]', 'High');
        await Promise.all([
            page.waitForNavigation({ waitUntil: 'networkidle0' }),
            page.click('button[type="submit"]')
        ]);
        await sleep(500);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '06_assignments_filtered.png'), fullPage: false });

        // 8. Exams Page
        console.log('Capturing Exams Page...');
        await page.goto(`${BASE_URL}/exams`, { waitUntil: 'networkidle0' });
        await sleep(500);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '07_exams.png'), fullPage: false });

        // 9. Settings Page
        console.log('Capturing Settings Page...');
        await page.goto(`${BASE_URL}/settings`, { waitUntil: 'networkidle0' });
        await sleep(500);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '08_settings.png'), fullPage: false });

        console.log('All UI screenshots captured successfully!');
    } catch (err) {
        console.error('Error during capture:', err);
    } finally {
        await browser.close();
    }
}

capture();
