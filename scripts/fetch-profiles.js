const fs = require('fs');
const puppeteer = require('puppeteer');

function parseCookies(cookiePath) {
    const cookies = [];
    const content = fs.readFileSync(cookiePath, 'utf8');
    const lines = content.split('\n');
    for (let line of lines) {
        if (line.trim() === '' || line.startsWith('#')) continue;
        const parts = line.split('\t');
        if (parts.length >= 7) {
            let domain = parts[0];
            if (domain.startsWith('#HttpOnly_')) domain = domain.substring(10);
            cookies.push({
                domain: domain,
                path: parts[2],
                secure: parts[3] === 'TRUE',
                expires: parseInt(parts[4]),
                name: parts[5],
                value: parts[6].trim()
            });
        }
    }
    return cookies;
}

(async () => {
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();
    const site = process.argv[2];

    try {
        if (site === 'x') {
            const cookies = parseCookies('secrets/cookies-x.txt');
            await page.setCookie(...cookies);
            await page.goto('https://x.com/', { waitUntil: 'networkidle2' });
            // Extract username
            const username = await page.evaluate(() => {
                const el = document.querySelector('a[aria-label="Profile"]');
                return el ? el.getAttribute('href').replace('/', '') : null;
            });
            console.log("X_USERNAME:" + username);
        }
        else if (site === 'reddit') {
            const cookies = parseCookies('secrets/cookies-reddit.txt');
            await page.setCookie(...cookies);
            await page.goto('https://www.reddit.com/', { waitUntil: 'networkidle2' });
            const username = await page.evaluate(() => {
                const el = document.querySelector('faceplate-tracker[source="nav"][action="click"][noun="profile"] a');
                return el ? el.getAttribute('href').replace('/user/', '').replace('/', '') : null;
            });
            console.log("REDDIT_USERNAME:" + username);
        }
        else if (site === 'pinterest') {
            const cookies = parseCookies('secrets/cookies-pinterest.txt');
            await page.setCookie(...cookies);
            await page.goto('https://www.pinterest.com/', { waitUntil: 'networkidle2' });
            const username = await page.evaluate(() => {
                const els = document.querySelectorAll('a');
                for (let el of els) {
                    if (el.href && el.href.includes('pinterest.com/') && !el.href.includes('/business/') && !el.href.includes('/settings/') && el.getAttribute('data-test-id') === 'header-profile') {
                        let url = new URL(el.href);
                        return url.pathname.replace(/\//g, '');
                    }
                }
                return null;
            });
            console.log("PINTEREST_USERNAME:" + username);
        }
        else if (site === 'medium') {
            const cookies = parseCookies('secrets/cookies-medium.txt');
            await page.setCookie(...cookies);
            await page.goto('https://medium.com/', { waitUntil: 'networkidle2' });
            const username = await page.evaluate(() => {
                const el = document.querySelector('a[aria-label="Profile"]');
                if (el) {
                    let url = new URL(el.href);
                    return url.pathname.replace('/', '');
                }
                return null;
            });
            console.log("MEDIUM_USERNAME:" + username);
        }
        else if (site === 'quora') {
            const cookies = parseCookies('secrets/cookies-quora.txt');
            await page.setCookie(...cookies);
            await page.goto('https://www.quora.com/', { waitUntil: 'networkidle2' });
            const username = await page.evaluate(() => {
                const el = document.querySelector('.q-box a[href*="/profile/"]');
                if (el) {
                    let url = new URL(el.href);
                    return url.pathname.replace('/profile/', '');
                }
                return null;
            });
            console.log("QUORA_USERNAME:" + username);
        }
    } catch (e) {
        console.error("ERROR:" + e.message);
    } finally {
        await browser.close();
    }
})();
