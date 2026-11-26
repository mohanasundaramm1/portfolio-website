/**
 * Live GitHub activity: summary line and contribution heatmap.
 * Reads data/github_activity.json, which scripts/github_activity_pipeline.py refreshes weekly.
 */
(function () {
    const PROFILE = 'https://github.com/mohanasundaramm1';
    const statsEl = document.getElementById('github-stats');
    if (!statsEl) return;

    fetch('data/github_activity.json')
        .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(renderStats)
        .catch(() => {
            statsEl.innerHTML = `<p class="muted">Activity data is unavailable right now.
                See it on <a href="${PROFILE}" target="_blank" rel="noopener">GitHub</a>.</p>`;
        });

    function renderStats(data) {
        const c = data.contributions;
        if (!c || !c.days || !c.days.length) {
            statsEl.innerHTML = `<p class="muted">See recent work on <a href="${PROFILE}" target="_blank" rel="noopener">GitHub</a>.</p>`;
            return;
        }
        const busiest = busiestMonth(c.days);
        const lastActive = [...c.days].reverse().find((d) => d.count > 0);
        const langs = (data.languages || []).filter((l) => l.name !== 'HTML').slice(0, 3).map((l) => l.name);
        const dot = '<span class="dot" aria-hidden="true">·</span>';

        statsEl.innerHTML = `
            <p class="activity-line">
                <span><b>${c.total.toLocaleString()}</b> contributions in the past year</span>${dot}
                <span><b>${data.summary.total_repos}</b> public repositories</span>${dot}
                <span>Busiest month: <b>${busiest.label}</b></span>${dot}
                <span>Last contribution: <b>${lastActive ? relative(lastActive.date) : '—'}</b></span>
            </p>
            <div class="heatmap-wrap" tabindex="0" aria-label="Contribution calendar for the past year">
                <div class="heatmap" role="img" aria-label="${c.total} contributions over the past year">${heatmap(c.days)}</div>
            </div>
            <div class="heatmap-foot">
                <span>${langs.length ? 'Mostly ' + langs.join(', ') : ''}</span>
                <span class="legend" aria-hidden="true">Less
                    <span class="day" data-level="0"></span><span class="day" data-level="1"></span><span class="day" data-level="2"></span><span class="day" data-level="3"></span><span class="day" data-level="4"></span>
                More</span>
            </div>`;

        // On narrow screens, start the calendar at the most recent weeks
        const wrap = statsEl.querySelector('.heatmap-wrap');
        wrap.scrollLeft = wrap.scrollWidth;
    }

    function heatmap(days) {
        const cells = [];
        const first = new Date(days[0].date + 'T00:00:00');
        for (let i = 0; i < first.getDay(); i++) cells.push({ pad: true });
        days.forEach((d) => cells.push(d));

        const cols = Math.ceil(cells.length / 7);
        let html = '';
        let lastMonth = -1;
        for (let col = 0; col < cols; col++) {
            const week = cells.slice(col * 7, col * 7 + 7);
            const firstReal = week.find((d) => !d.pad);
            const m = firstReal ? new Date(firstReal.date + 'T00:00:00').getMonth() : lastMonth;
            const label = m !== lastMonth && col < cols - 2
                ? new Date(2000, m, 1).toLocaleString('en-US', { month: 'short' }) : '';
            lastMonth = m;
            html += `<span class="month" style="grid-column:${col + 1}">${label}</span>`;
            week.forEach((d, row) => {
                const pos = `grid-column:${col + 1};grid-row:${row + 2}`;
                html += d.pad
                    ? `<span style="${pos}"></span>`
                    : `<span class="day" data-level="${d.level}" style="${pos}" title="${d.count} contribution${d.count === 1 ? '' : 's'} on ${fmt(d.date)}"></span>`;
            });
        }
        return html;
    }

    // ── Helpers ────────────────────────────────────────────────
    function busiestMonth(days) {
        const totals = {};
        days.forEach((d) => { const k = d.date.slice(0, 7); totals[k] = (totals[k] || 0) + d.count; });
        const [key] = Object.entries(totals).sort((a, b) => b[1] - a[1])[0];
        const [y, m] = key.split('-').map(Number);
        return { label: new Date(y, m - 1, 1).toLocaleString('en-US', { month: 'short', year: 'numeric' }) };
    }

    function fmt(iso) {
        return new Date(iso + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }

    function relative(iso) {
        const days = Math.round((new Date().setHours(0, 0, 0, 0) - new Date(iso + 'T00:00:00')) / 864e5);
        if (days <= 0) return 'today';
        if (days === 1) return 'yesterday';
        if (days < 7) return `${days} days ago`;
        if (days < 30) return `${Math.round(days / 7)} wk ago`;
        if (days < 365) return `${Math.round(days / 30)} mo ago`;
        return fmt(iso);
    }
})();
