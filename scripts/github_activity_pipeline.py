#!/usr/bin/env python3
"""
GitHub Activity Pipeline v2
Fetches comprehensive GitHub data: repos, events, languages, and contribution stats.
Uses multiple API endpoints for a complete picture.
"""

import json
import os
import re
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional
import urllib.request
import urllib.error


class GitHubActivityPipeline:
    """Extract, transform, and load GitHub activity data."""

    def __init__(self, username: str, token: Optional[str] = None):
        self.username = username
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHubActivityPipeline/2.0",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"

    def _http_get(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """GET a URL and return the body as text."""
        try:
            req = urllib.request.Request(url, headers=headers or {"User-Agent": self.headers["User-Agent"]})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode()
        except Exception as e:
            print(f"  ⚠️  Request failed for {url}: {e}")
            return None

    def _api_get(self, url: str) -> Optional[any]:
        """Make a GET request to the GitHub API."""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.URLError as e:
            print(f"  ⚠️  API error for {url}: {e}")
            return None
        except Exception as e:
            print(f"  ⚠️  Unexpected error: {e}")
            return None

    # ── Extract ──────────────────────────────────────────────────

    def extract_repos(self) -> List[Dict]:
        """Fetch all public repos with metadata."""
        repos = []
        page = 1
        while True:
            url = (
                f"{self.base_url}/users/{self.username}/repos"
                f"?per_page=100&page={page}&sort=updated&type=owner"
            )
            batch = self._api_get(url)
            if not batch:
                break
            repos.extend(batch)
            if len(batch) < 100:
                break
            page += 1

        print(f"  📦 Found {len(repos)} repositories")
        return repos

    def extract_events(self, days: int = 90) -> List[Dict]:
        """Fetch recent public events (paginated, up to 300)."""
        all_events = []
        cutoff = datetime.now() - timedelta(days=days)

        for page in range(1, 4):  # GitHub caps at 10 pages / 300 events
            url = (
                f"{self.base_url}/users/{self.username}/events/public"
                f"?per_page=100&page={page}"
            )
            events = self._api_get(url)
            if not events:
                break

            for ev in events:
                created = datetime.strptime(ev["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                if created > cutoff:
                    all_events.append(ev)

            if len(events) < 100:
                break

        print(f"  📡 Found {len(all_events)} events in last {days} days")
        return all_events

    def extract_contributions(self) -> List[Dict]:
        """Fetch the last year's contribution calendar.

        The calendar includes private contributions when the profile setting
        "Include private contributions" is on, so private work is counted
        without exposing any private repository. Tries the GraphQL API first,
        then falls back to the public contributions page.
        """
        days = self._contributions_graphql() or self._contributions_html()
        total = sum(d["count"] for d in days)
        print(f"  🟩 Found {total} contributions over {len(days)} days")
        return days

    def _contributions_graphql(self) -> List[Dict]:
        if "Authorization" not in self.headers:
            return []
        query = (
            '{ user(login: "%s") { contributionsCollection { contributionCalendar '
            "{ weeks { contributionDays { date contributionCount } } } } } }" % self.username
        )
        try:
            req = urllib.request.Request(
                f"{self.base_url}/graphql",
                data=json.dumps({"query": query}).encode(),
                headers={**self.headers, "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = json.loads(resp.read().decode())
            weeks = body["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
            return [
                {"date": d["date"], "count": d["contributionCount"]}
                for w in weeks
                for d in w["contributionDays"]
            ]
        except Exception as e:
            print(f"  ⚠️  GraphQL contributions unavailable ({e}); using public page")
            return []

    def _contributions_html(self) -> List[Dict]:
        html = self._http_get(f"https://github.com/users/{self.username}/contributions")
        if not html:
            return []
        dates = dict(re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*id="(contribution-day-component-[\d-]+)"', html))
        ids = {v: k for k, v in dates.items()}
        days = []
        for cid, text in re.findall(r'<tool-tip[^>]*for="(contribution-day-component-[\d-]+)"[^>]*>([^<]*)</tool-tip>', html):
            if cid not in ids:
                continue
            m = re.match(r"(\d+) contribution", text)
            days.append({"date": ids[cid], "count": int(m.group(1)) if m else 0})
        return sorted(days, key=lambda d: d["date"])

    # ── Transform ────────────────────────────────────────────────

    @staticmethod
    def transform_contributions(days: List[Dict]) -> Dict:
        """Summarize the calendar: totals, active days, streaks, intensity levels."""
        if not days:
            return {}
        counts = sorted(d["count"] for d in days if d["count"] > 0)

        def level(c: int) -> int:
            if c == 0 or not counts:
                return 0
            q = [counts[int(len(counts) * f)] for f in (0.25, 0.5, 0.75)]
            return 1 + sum(c > t for t in q)

        longest = run = 0
        for d in days:
            run = run + 1 if d["count"] > 0 else 0
            longest = max(longest, run)
        current = 0
        today = date.today().isoformat()
        for d in reversed(days):
            if d["date"] == today and d["count"] == 0:
                continue  # today isn't over yet
            if d["count"] == 0:
                break
            current += 1
        return {
            "total": sum(d["count"] for d in days),
            "active_days": sum(1 for d in days if d["count"] > 0),
            "longest_streak": longest,
            "current_streak": current,
            "busiest_day": max(days, key=lambda d: d["count"]),
            "includes_private": True,
            "days": [{**d, "level": level(d["count"])} for d in days],
        }

    def transform(self, repos: List[Dict], events: List[Dict]) -> Dict:
        """Combine repo + event data into a rich summary."""

        # ── Repo metrics ──
        languages: Dict[str, int] = {}
        total_stars = 0
        total_forks = 0
        repo_details = []

        for r in repos:
            if r.get("fork"):
                continue  # skip forks

            lang = r.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1

            total_stars += r.get("stargazers_count", 0)
            total_forks += r.get("forks_count", 0)

            repo_details.append({
                "name": r["full_name"],
                "description": r.get("description", ""),
                "language": lang or "N/A",
                "stars": r.get("stargazers_count", 0),
                "forks": r.get("forks_count", 0),
                "updated": r["updated_at"][:10],
                "pushed": (r.get("pushed_at") or r["updated_at"])[:10],
                "url": r["html_url"],
            })

        # Sort repos: most recently updated first
        repo_details.sort(key=lambda x: x["pushed"], reverse=True)

        # ── Event metrics ──
        commits_by_date: Dict[str, int] = {}
        event_types: Dict[str, int] = {}
        repos_from_events = set()
        total_commits = 0

        for ev in events:
            etype = ev["type"]
            day = ev["created_at"][:10]
            repo_name = ev["repo"]["name"]

            event_types[etype] = event_types.get(etype, 0) + 1
            repos_from_events.add(repo_name)

            if etype == "PushEvent":
                # Use distinct_size for actual unique commits, fallback to size
                payload = ev.get("payload", {})
                n = payload.get("distinct_size") or payload.get("size") or len(payload.get("commits", [])) or 1
                commits_by_date[day] = commits_by_date.get(day, 0) + n
                total_commits += n

        daily_activity = [
            {"date": d, "commits": c}
            for d, c in sorted(commits_by_date.items())
        ]

        # ── Language breakdown (sorted) ──
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)

        return {
            "summary": {
                "total_repos": len([r for r in repos if not r.get("fork")]),
                "total_stars": total_stars,
                "total_forks": total_forks,
                "total_commits": total_commits,
                "total_events": len(events),
                "most_active_event": (
                    max(event_types.items(), key=lambda x: x[1])[0]
                    if event_types
                    else "None"
                ),
            },
            "languages": [
                {"name": lang, "count": cnt} for lang, cnt in sorted_langs
            ],
            "daily_activity": daily_activity,
            "event_breakdown": event_types,
            "repos": repo_details,
            "last_updated": datetime.now().isoformat(),
        }

    # ── Load ─────────────────────────────────────────────────────

    def load(self, data: Dict, output_path: str):
        """Save transformed data to JSON."""
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        s = data["summary"]
        print(f"  ✅ Saved to {output_path}")
        print(f"     Repos: {s['total_repos']}  |  Stars: {s['total_stars']}  |  Commits: {s['total_commits']}")

    # ── Run ──────────────────────────────────────────────────────

    def run(self, output_path: str = "data/github_activity.json", days: int = 90):
        """Execute the full ETL pipeline."""
        print(f"🚀 GitHub Activity Pipeline v2 — @{self.username}")
        print(f"   Lookback: {days} days\n")

        repos = self.extract_repos()
        events = self.extract_events(days)
        data = self.transform(repos, events)
        data["contributions"] = self.transform_contributions(self.extract_contributions())
        self.load(data, output_path)

        print("\n✅ Pipeline complete!")


if __name__ == "__main__":
    USERNAME = "mohanasundaramm1"
    TOKEN = os.getenv("GITHUB_TOKEN")
    OUTPUT = "data/github_activity.json"

    days = 120
    pipeline = GitHubActivityPipeline(USERNAME, TOKEN)
    pipeline.run(OUTPUT, days=days)
