# GitHub Profile Analyzer

A Python script that pulls public data from the GitHub API and generates a readable summary report: top languages, top repositories, activity overview.

## The problem it solves

This demonstrates the same pattern businesses pay for constantly: connect to an API (GitHub here, but the same approach works for Stripe, a CRM, a marketing platform, etc.), pull the relevant data, and turn it into a clean, human-readable report — automatically, without manual copy-pasting.

## What it does

- Fetches user profile data and all public repositories via the GitHub REST API
- Aggregates language usage across all repos
- Ranks top repositories by stars
- Handles errors gracefully (invalid username, API rate limits, network issues)
- Outputs a clean Markdown report

## Usage

```bash
python github_analyzer.py <github-username> --output report.md
```

Example:
```bash
python github_analyzer.py torvalds --output torvalds_report.md
```

## Tech

Pure Python standard library (`urllib`) — no dependencies to install. Uses the public GitHub REST API (unauthenticated requests are rate-limited by GitHub; adding a personal access token easily raises the limit for production use).

## Author

Joness Tadjo — jonesstadjo@gmail.com
