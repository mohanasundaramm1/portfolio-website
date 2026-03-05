// GitHub Activity Visualization v2
// Renders repo cards, language breakdown, and activity stats from pipeline data

document.addEventListener('DOMContentLoaded', function () {
    fetch('data/github_activity.json')
        .then(response => {
            if (!response.ok) throw new Error('Failed to load activity data');
            return response.json();
        })
        .then(data => {
            renderActivityStats(data);
            renderRecentRepos(data);
        })
        .catch(error => {
            console.error('Error loading GitHub activity:', error);
            const container = document.getElementById('github-stats');
            if (container) {
                container.innerHTML = `
                    <p style="color:var(--slate-light); text-align:center;">
                        Unable to load GitHub activity data.
                    </p>`;
            }
        });
});

function renderActivityStats(data) {
    const statsContainer = document.getElementById('github-stats');
    if (!statsContainer) return;

    const { summary, event_breakdown, languages } = data;

    // Use push events as the main "contributions" metric since commit counts
    // from the events API are unreliable
    const pushEvents = event_breakdown.PushEvent || 0;
    const createEvents = event_breakdown.CreateEvent || 0;

    // Build language badges
    const langHTML = (languages || [])
        .slice(0, 6)
        .map(l => `<span class="lang-badge">${l.name}</span>`)
        .join('');

    statsContainer.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card glass-card">
                <div class="stat-number">${summary.total_repos}</div>
                <div class="stat-label">Repositories</div>
            </div>
            <div class="stat-card glass-card">
                <div class="stat-number">${pushEvents}</div>
                <div class="stat-label">Push Events</div>
            </div>
            <div class="stat-card glass-card">
                <div class="stat-number">${summary.total_stars}</div>
                <div class="stat-label">Stars</div>
            </div>
            <div class="stat-card glass-card">
                <div class="stat-number">${summary.total_events}</div>
                <div class="stat-label">Total Events</div>
            </div>
        </div>
        ${langHTML ? `<div class="lang-badges">${langHTML}</div>` : ''}
    `;
}

function renderRecentRepos(data) {
    const reposContainer = document.getElementById('recent-repos');
    if (!reposContainer) return;

    // Show top 6 most recently updated repos (skip portfolio-website itself)
    const repos = (data.repos || [])
        .filter(r => !r.name.includes('portfolio-website'))
        .slice(0, 6);

    if (repos.length === 0) {
        reposContainer.innerHTML = '<p style="color:var(--slate);">No repositories found.</p>';
        return;
    }

    const reposHTML = repos.map(repo => {
        const repoName = repo.name.split('/').pop();
        const desc = repo.description
            ? `<p class="repo-desc">${truncate(repo.description, 100)}</p>`
            : '';
        const langDot = repo.language && repo.language !== 'N/A'
            ? `<span class="repo-lang"><span class="lang-dot" style="background:${langColor(repo.language)}"></span>${repo.language}</span>`
            : '';

        return `
            <a href="${repo.url}" target="_blank" rel="noopener noreferrer" class="repo-card glass-card">
                <div class="repo-card-header">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                         fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                    </svg>
                    <h4 class="repo-name">${repoName}</h4>
                </div>
                ${desc}
                <div class="repo-meta">
                    ${langDot}
                    ${repo.stars > 0 ? `<span class="repo-stars">⭐ ${repo.stars}</span>` : ''}
                    <span class="repo-updated">Updated ${formatDate(repo.updated)}</span>
                </div>
            </a>
        `;
    }).join('');

    // Wrap in a grid
    reposContainer.innerHTML = `<div class="repos-grid">${reposHTML}</div>`;

    // Show last updated timestamp
    if (data.last_updated) {
        const ts = new Date(data.last_updated);
        reposContainer.insertAdjacentHTML('beforeend',
            `<p class="last-updated">Last updated: ${ts.toLocaleDateString('en-US', {
                year: 'numeric', month: 'short', day: 'numeric'
            })}</p>`
        );
    }
}

// ── Helpers ──────────────────────────────────────────────────

function truncate(str, max) {
    return str.length > max ? str.slice(0, max).trimEnd() + '…' : str;
}

function formatDate(dateStr) {
    const d = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now - d) / (1000 * 60 * 60 * 24));
    if (diff === 0) return 'today';
    if (diff === 1) return 'yesterday';
    if (diff < 7) return `${diff} days ago`;
    if (diff < 30) return `${Math.floor(diff / 7)} weeks ago`;
    if (diff < 365) return `${Math.floor(diff / 30)} months ago`;
    return dateStr;
}

function langColor(lang) {
    const colors = {
        'Python': '#3572A5',
        'JavaScript': '#f1e05a',
        'HTML': '#e34c26',
        'CSS': '#563d7c',
        'Jupyter Notebook': '#DA5B0B',
        'R': '#198CE7',
        'Shell': '#89e051',
        'TypeScript': '#3178c6',
        'Java': '#b07219',
        'Go': '#00ADD8',
    };
    return colors[lang] || '#64ffda';
}
