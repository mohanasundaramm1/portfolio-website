#!/usr/bin/env python3
"""
GitHub Activity Pipeline
Fetches recent GitHub activity (commits, PRs, repos) and generates JSON for portfolio display.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
import urllib.request
import urllib.error


class GitHubActivityPipeline:
    """Extract, transform, and load GitHub activity data."""
    
    def __init__(self, username: str, token: str = None):
        """
        Initialize the pipeline.
        
        Args:
            username: GitHub username
            token: Optional GitHub personal access token for higher rate limits
        """
        self.username = username
        self.base_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def extract_events(self, days: int = 30) -> List[Dict]:
        """
        Extract recent GitHub events for the user.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of event dictionaries
        """
        url = f"{self.base_url}/users/{self.username}/events/public?per_page=100"
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req) as response:
                events = json.loads(response.read().decode())
            
            # Filter events within the date range
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_events = [
                event for event in events
                if datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ') > cutoff_date
            ]
            
            return filtered_events
        except urllib.error.URLError as e:
            print(f"Error fetching events: {e}")
            return []
    
    def transform_events(self, events: List[Dict]) -> Dict:
        """
        Transform raw events into aggregated metrics.
        
        Args:
            events: List of raw GitHub events
            
        Returns:
            Dictionary with aggregated metrics
        """
        # Initialize counters
        commits_by_date = {}
        repos_touched = set()
        event_types = {}
        
        for event in events:
            event_type = event['type']
            created_at = event['created_at'][:10]  # YYYY-MM-DD
            repo_name = event['repo']['name']
            
            # Count event types
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            # Track repos
            repos_touched.add(repo_name)
            
            # Count commits per day (from PushEvent)
            if event_type == 'PushEvent':
                commit_count = len(event['payload'].get('commits', []))
                commits_by_date[created_at] = commits_by_date.get(created_at, 0) + commit_count
        
        # Calculate summary stats
        total_commits = sum(commits_by_date.values())
        total_repos = len(repos_touched)
        
        # Prepare daily activity for charting
        daily_activity = [
            {"date": date, "commits": count}
            for date, count in sorted(commits_by_date.items())
        ]
        
        return {
            "summary": {
                "total_commits": total_commits,
                "total_repos": total_repos,
                "total_events": len(events),
                "most_active_event": max(event_types.items(), key=lambda x: x[1])[0] if event_types else "None"
            },
            "daily_activity": daily_activity,
            "event_breakdown": event_types,
            "repos": list(repos_touched),
            "last_updated": datetime.now().isoformat()
        }
    
    def load_data(self, data: Dict, output_path: str):
        """
        Save transformed data to JSON file.
        
        Args:
            data: Transformed data dictionary
            output_path: Path to output JSON file
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Data saved to {output_path}")
        print(f"   Total commits: {data['summary']['total_commits']}")
        print(f"   Total repos: {data['summary']['total_repos']}")
    
    def run(self, output_path: str = "data/github_activity.json", days: int = 30):
        """
        Execute the full ETL pipeline.
        
        Args:
            output_path: Path to output JSON file
            days: Number of days to look back
        """
        print(f"🚀 Starting GitHub Activity Pipeline for @{self.username}")
        print(f"   Looking back {days} days...")
        
        # Extract
        events = self.extract_events(days)
        print(f"📥 Extracted {len(events)} events")
        
        # Transform
        data = self.transform_events(events)
        print(f"🔄 Transformed data")
        
        # Load
        self.load_data(data, output_path)
        print(f"✅ Pipeline complete!")


if __name__ == "__main__":
    # Configuration
    GITHUB_USERNAME = "mohanasundaramm1"
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Optional: Set via environment variable
    OUTPUT_PATH = "data/github_activity.json"
    
    # Run pipeline
    pipeline = GitHubActivityPipeline(GITHUB_USERNAME, GITHUB_TOKEN)
    pipeline.run(OUTPUT_PATH)
