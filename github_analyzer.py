#!/usr/bin/env python3
"""
GitHub Profile Analyzer
------------------------
Pulls public data from the GitHub API for a given username and generates
a summary report: top repositories, languages used, activity overview.

Real-world use case: this same pattern (call an API, aggregate the data,
output a clean report) is exactly what businesses pay for when they need
to pull data from Stripe, a CRM, a marketing platform, etc. and turn it
into something readable.

Usage:
    python github_analyzer.py octocat --output octocat_report.md
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from collections import Counter
from datetime import datetime


API_BASE = "https://api.github.com"


def fetch_json(url):
    """Fetch and parse JSON from a URL, with basic error handling."""
    req = urllib.request.Request(url, headers={"User-Agent": "github-analyzer-script"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit(f"Error: GitHub user not found.")
        elif e.code == 403:
            sys.exit("Error: API rate limit reached. Try again later.")
        else:
            sys.exit(f"Error: GitHub API returned {e.code}")
    except urllib.error.URLError as e:
        sys.exit(f"Error: could not reach GitHub API ({e.reason})")


def get_user_data(username):
    return fetch_json(f"{API_BASE}/users/{username}")


def get_repos(username):
    return fetch_json(f"{API_BASE}/users/{username}/repos?per_page=100&sort=updated")


def analyze_repos(repos):
    """Aggregate language usage, star counts, and activity from repo list."""
    languages = Counter()
    total_stars = 0
    total_forks = 0

    for repo in repos:
        if repo.get("language"):
            languages[repo["language"]] += 1
        total_stars += repo.get("stargazers_count", 0)
        total_forks += repo.get("forks_count", 0)

    top_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:5]

    return {
        "languages": languages.most_common(),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "top_repos": top_repos,
        "repo_count": len(repos),
    }


def generate_report(user, analysis, username):
    lines = []
    lines.append(f"# GitHub Profile Report: {username}")
    lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    lines.append("## Overview")
    lines.append(f"- **Name:** {user.get('name') or 'N/A'}")
    lines.append(f"- **Public repos:** {user.get('public_repos', 0)}")
    lines.append(f"- **Followers:** {user.get('followers', 0)}")
    lines.append(f"- **Account created:** {user.get('created_at', 'N/A')[:10]}")
    lines.append(f"- **Total stars across repos:** {analysis['total_stars']}")
    lines.append(f"- **Total forks across repos:** {analysis['total_forks']}\n")

    lines.append("## Top Languages")
    if analysis["languages"]:
        for lang, count in analysis["languages"][:8]:
            lines.append(f"- {lang}: {count} repo(s)")
    else:
        lines.append("- No language data available")
    lines.append("")

    lines.append("## Top 5 Repositories (by stars)")
    for repo in analysis["top_repos"]:
        stars = repo.get("stargazers_count", 0)
        desc = repo.get("description") or "No description"
        lines.append(f"- **{repo['name']}** ({stars} stars) — {desc}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze a public GitHub profile via the GitHub API.")
    parser.add_argument("username", help="GitHub username to analyze")
    parser.add_argument("--output", default=None, help="Path for the output report (default: <username>_report.md)")
    args = parser.parse_args()

    output_path = args.output or f"{args.username}_report.md"

    print(f"Fetching data for '{args.username}'...")
    user = get_user_data(args.username)
    repos = get_repos(args.username)

    analysis = analyze_repos(repos)
    report = generate_report(user, analysis, args.username)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to {output_path}")


if __name__ == "__main__":
    main()
