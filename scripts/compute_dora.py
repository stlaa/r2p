#!/usr/bin/env python3
"""
Compute basic DORA metrics using the GitHub API (PyGithub).
This script calculates:
- Lead Time for Changes: time from PR opened to merged for merged PRs in timeframe
- Deployment Frequency: number of merges to the target branch (e.g., main) in timeframe

Usage:
  export GITHUB_TOKEN=...
  python scripts/compute_dora.py --repo owner/repo --start 2025-01-01 --end 2025-01-31

The script writes `dora-metrics.json` to the current directory.
"""
import argparse
import datetime
import os
import json
from dateutil import parser as dateparser
from github import Github


def iso(dt):
    return dt.isoformat()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True, help='owner/repo')
    parser.add_argument('--start', required=True, help='start date YYYY-MM-DD')
    parser.add_argument('--end', required=True, help='end date YYYY-MM-DD')
    parser.add_argument('--branch', default='main', help='branch to consider for deployment frequency')
    args = parser.parse_args()

    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token:
        raise SystemExit('GITHUB_TOKEN/ GH_TOKEN required in env to query GitHub API')

    gh = Github(token)
    repo = gh.get_repo(args.repo)
    start = dateparser.parse(args.start)
    end = dateparser.parse(args.end) + datetime.timedelta(days=1)

    # Lead Time for Changes: aggregated over merged PRs
    pulls = repo.get_pulls(state='closed', sort='updated', direction='desc')
    lead_times = []
    merged_count = 0
    for pr in pulls:
        if pr.merged and pr.merged_at:
            if pr.merged_at < start or pr.merged_at >= end:
                continue
            opened = pr.created_at
            merged = pr.merged_at
            delta = (merged - opened).total_seconds()
            lead_times.append(delta)
            merged_count += 1

    avg_lead_seconds = sum(lead_times) / len(lead_times) if lead_times else None

    # Deployment frequency (approximated as number of merges to branch)
    commits = repo.get_commits(since=start, until=end)
    deploy_count = 0
    for c in commits:
        try:
            # count commits whose ref includes the target branch name in commit message or associated with merges to branch
            # This is an approximation; for accurate deployment frequency integrate with deployment events
            if args.branch in (c.commit.message or ''):
                deploy_count += 1
        except Exception:
            continue

    results = {
        'start': args.start,
        'end': args.end,
        'lead_time_seconds_avg': avg_lead_seconds,
        'merged_pr_count': merged_count,
        'deployment_frequency_estimate': deploy_count,
        'generated_at': iso(datetime.datetime.utcnow())
    }

    out = 'dora-metrics.json'
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)

    print('Wrote', out)


if __name__ == '__main__':
    main()
