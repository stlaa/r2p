# CI/CD Merge Gating Setup Guide

This document provides step-by-step instructions to enable and manage the GitHub Actions CI/CD merge gating workflow for the **r2p** repository.

## Overview

The CI pipeline includes:
- **Containerization**: Docker image build for reproducible environments
- **Testing**: pytest with coverage reporting
- **Static Analysis**: ruff (linting) and bandit (security analysis)
- **Observability**: PR label updates and DORA metrics computation
- **Branch Protection**: Automated or manual enforcement of merge requirements

All workflows use reusable job patterns and no exposed secrets.

---

## 1. Initial Setup

### 1.1 Verify Workflows Are Visible

1. Go to your repository: `https://github.com/ashwinberyl/r2p`
2. Click **Actions** tab
3. You should see:
   - `CI` (triggered on PR open/sync)
   - `Update PR Labels Based on CI` (triggered when CI completes)
   - `DORA Metrics` (daily schedule + manual trigger)
   - `Set Branch Protection (manual)` (manual trigger)

If workflows don't appear, check that `.github/workflows/*.yml` files exist and are committed.

### 1.2 Set Up Secrets for Branch Protection (Optional but Recommended)

To enable automatic branch protection via the `Set Branch Protection (manual)` workflow:

1. **Create a Personal Access Token (PAT)**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click **Generate new token (classic)**
   - Name: `BRANCH_PROTECTION_TOKEN`
   - Select scopes:
     - `repo` (full control of private repositories)
     - `admin:repo_hook` (write access to hooks)
   - Copy the token (save it securely; GitHub won't show it again)

2. **Add the Secret to Your Repository**:
   - Go to your repository Settings → Secrets and variables → Actions
   - Click **New repository secret**
   - Name: `BRANCH_PROTECTION_TOKEN`
   - Value: (paste the PAT you created)
   - Click **Add secret**

**Note**: The `GITHUB_TOKEN` (automatically provided by GitHub Actions) is used for PR labeling and general CI checks. It has limited scope and cannot set branch protection; hence the separate `BRANCH_PROTECTION_TOKEN`.

---

## 2. Enable Branch Protection

### Option A: Automatic via Workflow (Recommended for CI Admins)

1. Go to **Actions** tab
2. Click **Set Branch Protection (manual)** in the left sidebar
3. Click **Run workflow**
4. Ensure:
   - Branch: `main` (or your default branch)
   - Confirm your `BRANCH_PROTECTION_TOKEN` secret is set (from step 1.2)
5. Click **Run workflow**

The workflow will apply these protections:
- Require all CI checks (`build`, `test`, `static-analysis`) to pass
- Require 1 approval on PRs
- Enforce protection for admins

### Option B: Manual via GitHub UI

1. Go to Settings → Branches
2. Under "Branch protection rules", click **Add rule**
3. Branch name pattern: `main`
4. Enable:
   - ✓ Require a pull request before merging
   - ✓ Require approvals (1)
   - ✓ Require status checks to pass before merging
     - Select: `build`, `test`, `static-analysis`
     - ✓ Require branches to be up to date before merging
   - ✓ Enforce for admins
5. Click **Create**

---

## 3. How CI Checks Work

### Workflow Trigger
- **On**: Pull request (opened, synchronized, reopened, ready for review)
- **Where**: `.github/workflows/ci.yml` orchestrates the jobs

### Job Sequence (Sequential with Dependencies)
```
build (no dependency)
  ↓
test (depends on build)
  ↓
static-analysis (depends on test)
  ↓
summarize (depends on all above)
```

Each job can fail independently, blocking merge. If any job fails, the PR cannot merge (enforced by branch protection).

### Job Details

| Job | Purpose | Files Checked | Duration |
|-----|---------|--------------|----------|
| **build** | Docker image build | `Dockerfile`, `requirements.txt` | ~1-2 min |
| **test** | pytest with coverage | Test files + app code | ~1-2 min |
| **static-analysis** | Linting & security | All `.py` files | ~30 sec |


---

## 4. PR Labeling

After CI completes, `update-pr-labels.yml` automatically applies labels:
- **`ci: passing`** – All checks passed (green)
- **`ci: failing`** – One or more checks failed (red)

These labels help quickly identify PR status without opening the "Checks" tab.

---

## 5. DORA Metrics

### What is DORA?

DORA (DevOps Research and Assessment) metrics measure deployment performance:
- **Lead Time for Changes**: Avg time from PR opened → merged
- **Deployment Frequency**: Number of merges/deployments per time period
- **Time to Restore**: Avg time to fix a failed deployment
- **Change Failure Rate**: % of deployments causing failure

### Compute Metrics

The workflow `dora-metrics.yml` runs:
- **Schedule**: Daily at 02:00 UTC
- **Manual trigger**: Go to Actions → DORA Metrics → Run workflow

**Output**: `dora-metrics.json` artifact containing:
```json
{
  "start": "2025-01-01",
  "end": "2025-01-08",
  "lead_time_seconds_avg": 86400,
  "merged_pr_count": 5,
  "deployment_frequency_estimate": 12,
  "generated_at": "2025-01-08T10:30:45.123456"
}
```

### Limitations & Extensions

The current `scripts/compute_dora.py` calculates:
- Lead time from merged PR creation → merge timestamp
- Deployment frequency as an estimate (commit message matching)

**For Production Use**, integrate with:
- GitHub Deployments API (if using GitHub Environments)
- CD tool webhooks (e.g., ArgoCD, Flux, Jenkins)
- Incident tracking system (for time-to-restore)

---

## 6. Security & No Exposed Secrets

### Best Practices
1. **Never commit secrets** – Use environment variables, GitHub Secrets, or a secret manager
2. **PAT tokens** – Use minimal-scope PATs (e.g., `BRANCH_PROTECTION_TOKEN` scoped to repo, not all orgs)
3. **Rotate tokens** – If a token ever leaks, GitHub can revoke it; update your secret immediately
4. **Use GitHub Secrets** – Store all sensitive values in repo/org Secrets; reference as `${{ secrets.NAME }}`

---

## 7. Troubleshooting

### CI Checks Fail but Everything Looks Good?

**Build failures**:
- Check Docker version: `docker --version`
- Ensure `Dockerfile` and `requirements.txt` are valid
- View full logs in the Action run

**Test failures**:
- Check `coverage-report` artifact for details
- Run locally: `pytest -q` in your Python environment

**Static analysis failures**:
- Ruff output shows style issues: fix with `ruff check . --fix`
- Bandit output shows security issues: review and fix or add ignores

### PR Can't Merge Despite Green Checks?

1. **Branch protection not updated** – Re-run `Set Branch Protection (manual)` or verify in Settings → Branches
2. **Status checks mismatch** – Ensure branch protection lists exactly: `build`, `test`, `static-analysis`
3. **Pending checks** – CI workflow may still be running; wait for all checks to show pass/fail
4. **Require up-to-date branches** – If enabled, rebase your branch on `main`

---

## 8. Local Development & Testing

### Run Docker Build Locally
```bash
docker build -t r2p:local .
docker run -p 5000:5000 r2p:local
```

### Run Tests Locally
```bash
pip install -r requirements.txt
pytest -q --cov=. --maxfail=1
```

### Run Security Checks Locally
```bash
# Install tools
pip install ruff bandit

# Run linting and security analysis
ruff check .
bandit -r .
```

---

## 9. Maintenance & Monitoring

### Weekly
- Review failed CI checks in PRs
- Check DORA metrics trend (if integrated)

### Monthly
- Rotate `BRANCH_PROTECTION_TOKEN` if possible
- Review & update linting/security rules in `.github/workflows/reusable/static-analysis.yml`

### Quarterly
- Update Python version in workflows (if needed)
- Review & upgrade container base image (currently `python:3.11-slim`)

---

## 10. Quick Reference

| Action | Link / Command |
|--------|---|
| View CI Workflows | `https://github.com/ashwinberyl/r2p/actions` |
| Add/Edit Secrets | Settings → Secrets and variables → Actions |
| Enable Branch Protection | Settings → Branches → Add rule |
| Rerun CI for PR | Actions tab → Select PR run → Re-run jobs |
| View DORA Metrics | Actions → DORA Metrics → Latest run artifacts |
| Manual Branch Protection | Actions → Set Branch Protection (manual) → Run workflow |

---

## 11. Support & Feedback

If workflows fail unexpectedly or you need adjustments:
1. Check the Action run logs for error details
2. Review this guide's Troubleshooting section
3. Update workflow YAML in `.github/workflows/` as needed
4. Commit changes and test on a feature branch

---

**Last Updated**: 2025-11-16  
**Maintained by**: DevOps Team
