/**
 * Main JavaScript File
 * Handles mobile navigation and future interactive elements.
 */

// Prevent auto-scroll on page load
if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
}

// Force scroll to top on page load
window.addEventListener('beforeunload', () => {
    window.scrollTo(0, 0);
});

document.addEventListener('DOMContentLoaded', () => {
    // Ensure page starts at top
    window.scrollTo(0, 0);

    console.log('Portfolio Site Loaded Successfully');

    // Future: Mobile Menu Toggle Logic
});
