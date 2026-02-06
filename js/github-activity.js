// GitHub Activity Visualization
document.addEventListener('DOMContentLoaded', function () {
    // Fetch GitHub activity data
    fetch('data/github_activity.json')
        .then(response => response.json())
        .then(data => {
            renderActivityStats(data);
            renderRecentRepos(data);
        })
        .catch(error => {
            console.error('Error loading GitHub activity:', error);
        });
});

function renderActivityStats(data) {
    const statsContainer = document.getElementById('github-stats');
    if (!statsContainer) return;

    const { summary, event_breakdown } = data;

    statsContainer.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card glass-card">
                <div class="stat-number">${summary.total_events}</div>
                <div class="stat-label">Recent Events</div>
            </div>
            <div class="stat-card glass-card">
                <div class="stat-number">${summary.total_repos}</div>
                <div class="stat-label">Active Repos</div>
            </div>
            <div class="stat-card glass-card">
                <div class="stat-number">${event_breakdown.PushEvent || 0}</div>
                <div class="stat-label">Push Events</div>
            </div>
            <div class="stat-card glass-card">
                <div class="stat-number">${event_breakdown.CreateEvent || 0}</div>
                <div class="stat-label">New Branches</div>
            </div>
        </div>
    `;
}

function renderRecentRepos(data) {
    const reposContainer = document.getElementById('recent-repos');
    if (!reposContainer) return;

    const repos = data.repos.slice(0, 5);

    const reposHTML = repos.map(repo => {
        const repoName = repo.split('/')[1];
        return `
            <div class="repo-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                </svg>
                <a href="https://github.com/${repo}" target="_blank">${repoName}</a>
            </div>
        `;
    }).join('');

    reposContainer.innerHTML = reposHTML;
}
