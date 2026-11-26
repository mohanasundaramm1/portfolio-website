/**
 * Site interactions: theme toggle, mobile menu, active nav link, copy email.
 */
(function () {
    const root = document.documentElement;

    // ── Theme toggle ───────────────────────────────────────────
    const themeBtn = document.getElementById('theme-toggle');
    const syncThemeLabel = () => {
        const dark = root.dataset.theme === 'dark';
        themeBtn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
        document.querySelector('meta[name="theme-color"]').content = dark ? '#0a1416' : '#ffffff';
    };
    themeBtn.addEventListener('click', () => {
        root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem('theme', root.dataset.theme); } catch (e) { /* private mode */ }
        syncThemeLabel();
    });
    syncThemeLabel();

    // ── Mobile menu ────────────────────────────────────────────
    const menuBtn = document.getElementById('menu-toggle');
    const links = document.getElementById('nav-links');
    const setMenu = (open) => {
        links.classList.toggle('open', open);
        menuBtn.setAttribute('aria-expanded', String(open));
        menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    menuBtn.addEventListener('click', () => setMenu(!links.classList.contains('open')));
    links.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

    // ── Header border once the page scrolls ────────────────────
    const header = document.querySelector('.site-header');
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // ── Highlight the nav link for the section in view ─────────
    const navLinks = [...links.querySelectorAll('a[href^="#"]')];
    // Every section is observed, so no link stays highlighted in sections outside the menu
    const sections = [...document.querySelectorAll('main > section[id]')];
    if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                navLinks.forEach((a) => {
                    const on = a.getAttribute('href') === '#' + entry.target.id;
                    a.classList.toggle('active', on);
                    if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
                });
            });
        }, { rootMargin: '-45% 0px -50% 0px' });
        sections.forEach((s) => io.observe(s));
    }

    // ── Copy email ─────────────────────────────────────────────
    const copyBtn = document.getElementById('copy-email');
    if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
            const label = copyBtn.querySelector('span');
            const original = label.textContent;
            try {
                await navigator.clipboard.writeText(copyBtn.dataset.email);
                label.textContent = 'Copied to clipboard';
            } catch (e) {
                label.textContent = copyBtn.dataset.email;
            }
            setTimeout(() => { label.textContent = original; }, 2500);
        });
    }

    // ── Fade sections in as they scroll into view ───────────────
    const reveals = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
        const ro = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in');
                    ro.unobserve(entry.target);
                }
            });
        }, { rootMargin: '0px 0px -8% 0px' });
        reveals.forEach((el, i) => {
            el.style.transitionDelay = `${(i % 4) * 70}ms`;
            ro.observe(el);
        });
    } else {
        reveals.forEach((el) => el.classList.add('in'));
    }

    document.getElementById('year').textContent = new Date().getFullYear();
})();
