#!/usr/bin/env python3
"""
GitHub Activity Pipeline v2
Fetches comprehensive GitHub data: repos, events, languages, and contribution stats.
Uses multiple API endpoints for a complete picture.
"""

import json
import os
from datetime import datetime, timedelta
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

    # ── Transform ────────────────────────────────────────────────

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
                "url": r["html_url"],
            })

        # Sort repos: most recently updated first
        repo_details.sort(key=lambda x: x["updated"], reverse=True)

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
        self.load(data, output_path)

        print("\n✅ Pipeline complete!")


if __name__ == "__main__":
    USERNAME = "mohanasundaramm1"
    TOKEN = os.getenv("GITHUB_TOKEN")
    OUTPUT = "data/github_activity.json"

    days = 120
    pipeline = GitHubActivityPipeline(USERNAME, TOKEN)
    pipeline.run(OUTPUT, days=days)
