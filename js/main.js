/**
 * Main JavaScript File
 * Handles mobile navigation and future interactive elements.
 */

// Immediate scroll to top (before anything else)
window.scrollTo(0, 0);

// Prevent auto-scroll on page load - Multiple strategies for cross-browser compatibility
if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
}

// Force scroll to top immediately and repeatedly
let scrollAttempts = 0;
const maxScrollAttempts = 10;
const scrollInterval = setInterval(() => {
    window.scrollTo(0, 0);
    scrollAttempts++;
    if (scrollAttempts >= maxScrollAttempts) {
        clearInterval(scrollInterval);
    }
}, 50); // Check every 50ms for the first 500ms

// Additional scroll prevention on page show (handles back/forward navigation)
window.addEventListener('pageshow', (event) => {
    window.scrollTo(0, 0);
});

// Force scroll to top on page load
window.addEventListener('load', () => {
    window.scrollTo(0, 0);
    // Double-check after a short delay
    setTimeout(() => {
        window.scrollTo(0, 0);
    }, 100);
});

// Reset scroll before unload
window.addEventListener('beforeunload', () => {
    window.scrollTo(0, 0);
});

document.addEventListener('DOMContentLoaded', () => {
    // Ensure page starts at top
    window.scrollTo(0, 0);

    console.log('Portfolio Site Loaded Successfully');

    // Future: Mobile Menu Toggle Logic
});
